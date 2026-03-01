import json
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .emailing import EmailDeliveryError, send_email_message
from .models import EmailVerificationToken, User


def parse_json_body(request: HttpRequest) -> dict:
    if not request.body:
        return {}

    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload.")


def serialize_user(user: User) -> dict:
    return {"id": str(user.id), "email": user.email, "email_verified": user.email_verified}


def build_verification_link(token: str) -> str:
    return f"{settings.FRONTEND_APP_URL.rstrip('/')}/verify-email/{token}"


def create_email_verification_token(user: User) -> EmailVerificationToken:
    token, _ = EmailVerificationToken.objects.update_or_create(
        user=user,
        defaults={
            "expires_at": timezone.now()
            + timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS),
        },
    )
    return token


def send_verification_email(user: User) -> None:
    token = create_email_verification_token(user)
    verification_link = build_verification_link(str(token.token))
    subject = "Verify your TrustDriver email"
    text = (
        "Welcome to TrustDriver.\n\n"
        f"Verify your email by opening this link:\n{verification_link}\n\n"
        f"This link expires in {settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS} hours."
    )
    html = (
        "<p>Welcome to TrustDriver.</p>"
        f"<p>Verify your email by opening this link:</p><p><a href=\"{verification_link}\">{verification_link}</a></p>"
        f"<p>This link expires in {settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS} hours.</p>"
    )

    send_email_message(to_email=user.email, subject=subject, text=text, html=html)


@csrf_exempt
def register_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "User already exists"}, status=400)

    try:
        with transaction.atomic():
            user = User.objects.create_user(email=email, password=password)
            send_verification_email(user)
    except EmailDeliveryError:
        return JsonResponse(
            {
                "error": "Unable to send the verification email right now. Please try again later.",
            },
            status=503,
        )

    return JsonResponse(
        {
            "success": True,
            "requiresEmailVerification": True,
            "email": user.email,
            "message": "Account created. Check your email to verify your address before signing in.",
        }
    )


@csrf_exempt
def login_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    user = authenticate(request, email=email, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    if not user.email_verified:
        return JsonResponse(
            {
                "error": "Verify your email before signing in.",
                "requiresEmailVerification": True,
                "email": user.email,
            },
            status=403,
        )

    login(request, user)
    return JsonResponse({"success": True, "user": serialize_user(user)})


@csrf_exempt
def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    logout(request)
    return JsonResponse({"success": True})


@csrf_exempt
def resend_verification_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    email = (payload.get("email") or "").strip().lower()
    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    user = User.objects.filter(email=email).first()
    if user is None:
        return JsonResponse(
            {
                "success": True,
                "message": "If that account exists, a verification email has been sent.",
            }
        )

    if user.email_verified:
        return JsonResponse({"error": "This email is already verified."}, status=400)

    try:
        send_verification_email(user)
    except EmailDeliveryError:
        return JsonResponse(
            {
                "error": "Unable to resend the verification email right now. Please try again later.",
            },
            status=503,
        )

    return JsonResponse(
        {
            "success": True,
            "message": "A new verification email has been sent.",
        }
    )


def verify_email_view(request: HttpRequest, token) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    verification_token = EmailVerificationToken.objects.filter(token=token).select_related("user").first()
    if verification_token is None:
        return JsonResponse({"error": "Invalid verification link."}, status=404)

    if verification_token.expires_at < timezone.now():
        verification_token.delete()
        return JsonResponse({"error": "This verification link has expired."}, status=400)

    user = verification_token.user
    user.email_verified = True
    user.save(update_fields=["email_verified"])
    verification_token.delete()

    return JsonResponse(
        {
            "success": True,
            "message": "Your email has been verified. You can now sign in.",
        }
    )


def me_view(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    if not request.user.email_verified:
        logout(request)
        return JsonResponse(
            {
                "error": "Verify your email before signing in.",
                "requiresEmailVerification": True,
                "email": request.user.email,
            },
            status=401,
        )

    return JsonResponse({"user": serialize_user(request.user)})
