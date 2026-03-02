import os
import sys
from pathlib import Path

# Ajouter le backend au path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

# Configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 70)
print("Configuration actuelle:")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD[:4]}****{settings.EMAIL_HOST_PASSWORD[-4:]}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print("=" * 70)

print("\n📧 Envoi d'un email de test...")

try:
    result = send_mail(
        subject="✅ Test TrustDriver",
        message="Si tu reçois cet email, la configuration fonctionne !",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print(f"\n✅ Email envoyé avec succès ! (résultat: {result})")
    print(f"Vérifie ta boîte mail : {settings.EMAIL_HOST_USER}")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    print("\nDiagnostic:")
    print("  • Vérifie que la 2FA est activée sur ton compte Google")
    print("  • Vérifie que l'App Password est correct")
    print("  • Essaie de générer un nouveau App Password")
