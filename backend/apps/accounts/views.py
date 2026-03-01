import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User


def parse_json_body(request: HttpRequest) -> dict:
    if not request.body:
        return {}

    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload.")


def serialize_user(user: User) -> dict:
    return {"id": str(user.id), "email": user.email}


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

    user = User.objects.create_user(email=email, password=password)
    login(request, user)
    return JsonResponse({"success": True, "user": serialize_user(user)})


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

    login(request, user)
    return JsonResponse({"success": True, "user": serialize_user(user)})


@csrf_exempt
def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    logout(request)
    return JsonResponse({"success": True})


def me_view(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    return JsonResponse({"user": serialize_user(request.user)})
