#!/usr/bin/env python
"""
Script de test pour vérifier l'envoi d'emails Django
Usage: python manage.py shell < scripts/test_email.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=" * 60)
    print("TEST D'ENVOI D'EMAIL DJANGO")
    print("=" * 60)
    print(f"\nConfiguration actuelle:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"\n{'=' * 60}")
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERREUR: EMAIL_HOST_USER ou EMAIL_HOST_PASSWORD non configuré")
        print("\nVérifie ton fichier backend/.env")
        return
    
    try:
        print("\n📧 Envoi d'un email de test...")
        
        send_mail(
            subject="✅ Test Django Email - TrustDriver",
            message="Félicitations ! Ton serveur Django peut envoyer des emails avec succès.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Envoie à toi-même
            fail_silently=False,
        )
        
        print(f"\n✅ Email envoyé avec succès à {settings.EMAIL_HOST_USER}")
        print("\nVérifie ta boîte de réception (et spam si besoin)")
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de l'envoi: {e}")
        print("\nErreurs courantes:")
        print("  • 535 Authentication failed → Mauvais App Password ou 2FA non activé")
        print("  • Connection refused → Mauvais port ou host")
        print("  • Timeout → Firewall ou proxy bloque le port 587")
        print("\nSolution:")
        print("  1. Va sur https://myaccount.google.com/security")
        print("  2. Active la Validation en 2 étapes")
        print("  3. Va dans 'Mots de passe des applications'")
        print("  4. Génère un nouveau mot de passe pour 'Mail / Django'")
        print("  5. Mets-le dans EMAIL_HOST_PASSWORD dans backend/.env")

if __name__ == "__main__":
    test_email()
