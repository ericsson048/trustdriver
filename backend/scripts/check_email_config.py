#!/usr/bin/env python
"""
Vérifie la configuration email actuelle
Usage: python backend/scripts/check_email_config.py
"""
import os
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.conf import settings

print("=" * 70)
print("📧 CONFIGURATION EMAIL ACTUELLE")
print("=" * 70)

print("\n🔍 Backend utilisé :")
if settings.RESEND_API_KEY:
    print("   ⚠️  RESEND (API)")
    print(f"   API Key : {settings.RESEND_API_KEY[:10]}...****")
    print(f"   From    : {settings.RESEND_FROM_EMAIL}")
    print("\n   ⚠️  ATTENTION : Resend ne peut pas envoyer depuis @gmail.com")
    print("   Solution : Supprime RESEND_API_KEY pour utiliser Gmail SMTP")
else:
    print("   ✅ DJANGO SMTP (Gmail)")
    print(f"   Backend : {settings.EMAIL_BACKEND}")
    print(f"   Host    : {settings.EMAIL_HOST}")
    print(f"   Port    : {settings.EMAIL_PORT}")
    print(f"   User    : {settings.EMAIL_HOST_USER}")
    print(f"   Password: {settings.EMAIL_HOST_PASSWORD[:4]}****{settings.EMAIL_HOST_PASSWORD[-4:] if len(settings.EMAIL_HOST_PASSWORD) > 8 else '****'}")
    print(f"   TLS     : {settings.EMAIL_USE_TLS}")
    print(f"   From    : {settings.DEFAULT_FROM_EMAIL}")

print(f"\n🌐 Frontend URL : {settings.FRONTEND_APP_URL}")
print(f"⏰ Token TTL    : {settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS} heures")

print("\n" + "=" * 70)

if settings.RESEND_API_KEY:
    print("⚠️  PROBLÈME DÉTECTÉ")
    print("=" * 70)
    print("\nTu utilises Resend mais avec un email @gmail.com")
    print("Resend refuse d'envoyer depuis des domaines non vérifiés.")
    print("\n📋 SOLUTIONS :")
    print("\n1. Utiliser Gmail SMTP (recommandé pour l'instant) :")
    print("   - Sur Render : Supprime la variable RESEND_API_KEY")
    print("   - Ou mets RESEND_API_KEY='' (vide)")
    print("   - Redémarre le service")
    print("\n2. Configurer Resend correctement :")
    print("   - Va sur https://resend.com/domains")
    print("   - Ajoute et vérifie un domaine personnalisé")
    print("   - Ou utilise : RESEND_FROM_EMAIL=onboarding@resend.dev")
else:
    print("✅ CONFIGURATION OK")
    print("=" * 70)
    print("\nTu utilises Gmail SMTP, c'est parfait !")
    print("\n💡 Pour tester l'envoi :")
    print("   npm run test:email")
    print("   ou")
    print("   python backend/scripts/quick_test.py")
