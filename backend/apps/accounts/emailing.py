import json
from urllib import error, request

from django.conf import settings
from django.core.mail import send_mail


class EmailDeliveryError(RuntimeError):
    pass


def send_email_message(*, to_email: str, subject: str, text: str, html: str | None = None) -> None:
    if settings.RESEND_API_KEY:
        send_with_resend(to_email=to_email, subject=subject, text=text, html=html)
        return

    send_mail(
        subject=subject,
        message=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
        html_message=html,
    )


def send_with_resend(*, to_email: str, subject: str, text: str, html: str | None = None) -> None:
    payload = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": text,
    }
    if html:
        payload["html"] = html

    api_request = request.Request(
        url="https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=15) as response:
            if response.status < 200 or response.status >= 300:
                raise EmailDeliveryError("Resend rejected the email request.")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise EmailDeliveryError(f"Resend API error: {details or exc.reason}") from exc
    except error.URLError as exc:
        raise EmailDeliveryError(f"Unable to reach Resend: {exc.reason}") from exc
