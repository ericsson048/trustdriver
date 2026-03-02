#!/usr/bin/env python
"""
Test complet du flow d'inscription avec envoi d'email
Usage: python backend/scripts/test_registration_flow.py
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
from apps.accounts.models import User, EmailVerificationToken
from apps.accounts.views import send_verification_email

print("=" * 70)
print("🧪 TEST DU FLOW D'INSCRIPTION COMPLET")
print("=" * 70)

# Nettoyer les utilisateurs de test existants
test_email = "test@example.com"
User.objects.filter(email=test_email).delete()

print(f"\n1️⃣ Création d'un utilisateur test : {test_email}")
user = User.objects.create_user(
    email=test_email,
    password="testpass123"
)
print(f"   ✅ Utilisateur créé (ID: {user.id})")
print(f"   Email vérifié : {user.email_verified}")

print(f"\n2️⃣ Envoi de l'email de vérification...")
print(f"   Frontend URL : {settings.FRONTEND_APP_URL}")

try:
    send_verification_email(user)
    print(f"   ✅ Email envoyé avec succès !")
    
    # Récupérer le token
    token = EmailVerificationToken.objects.get(user=user)
    verification_link = f"{settings.FRONTEND_APP_URL.rstrip('/')}/verify-email/{token.token}"
    
    print(f"\n3️⃣ Détails du token de vérification :")
    print(f"   Token : {token.token}")
    print(f"   Expire : {token.expires_at}")
    print(f"   Lien  : {verification_link}")
    
    print(f"\n4️⃣ Vérification de l'email...")
    print(f"   📧 Vérifie ta boîte mail : {settings.EMAIL_HOST_USER}")
    print(f"   📧 Sujet : 'Verify your TrustDriver email'")
    print(f"   📧 Vérifie aussi le dossier spam si besoin")
    
    print(f"\n5️⃣ Pour simuler la vérification :")
    print(f"   python manage.py shell")
    print(f"   >>> from apps.accounts.models import EmailVerificationToken")
    print(f"   >>> token = EmailVerificationToken.objects.get(token='{token.token}')")
    print(f"   >>> user = token.user")
    print(f"   >>> user.email_verified = True")
    print(f"   >>> user.save()")
    print(f"   >>> token.delete()")
    
    print("\n" + "=" * 70)
    print("✅ TEST RÉUSSI - Le flow d'inscription fonctionne !")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERREUR lors de l'envoi : {e}")
    print("\nVérifie :")
    print("  • Que EMAIL_HOST_PASSWORD est correct dans backend/.env")
    print("  • Que la 2FA est activée sur ton compte Google")
    print("  • Que l'App Password est valide")
    
    import traceback
    traceback.print_exc()

print(f"\n💡 Pour nettoyer : User.objects.filter(email='{test_email}').delete()")
