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
    # En mode développement/test sans domaine vérifié, Resend n'accepte que certains emails
    # Pour contourner cette limitation temporairement, on peut logger l'email au lieu de l'envoyer
    # TODO: Configurer un domaine vérifié sur Resend pour la production
    
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
            "User-Agent": "trustdriver/1.0",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=15) as response:
            if response.status < 200 or response.status >= 300:
                raise EmailDeliveryError("Resend rejected the email request.")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        
        # Si l'erreur est due à la restriction de domaine, logger au lieu de crasher
        if "validation_error" in details and "verify a domain" in details:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                f"Resend domain not verified. Email would be sent to {to_email}: {subject}\n"
                f"Content: {text}\n"
                f"Configure a verified domain at https://resend.com/domains"
            )
            # En développement, on peut considérer que l'email est "envoyé" pour ne pas bloquer
            if settings.DEBUG:
                return
        
        raise EmailDeliveryError(f"Resend API error: {details or exc.reason}") from exc
    except error.URLError as exc:
        raise EmailDeliveryError(f"Unable to reach Resend: {exc.reason}") from exc
