#!/usr/bin/env python
"""
Test Resend directement avec la bibliothèque officielle
Usage: python backend/scripts/test_resend.py
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
print("🧪 TEST RESEND")
print("=" * 70)

print(f"\nAPI Key: {settings.RESEND_API_KEY[:10]}...****")
print(f"From: {settings.RESEND_FROM_EMAIL}")

try:
    import resend
    
    resend.api_key = settings.RESEND_API_KEY
    
    print("\n📧 Envoi d'un email de test via Resend...")
    
    params = {
        "from": "TrustDriver <onboarding@resend.dev>",
        "to": ["edulms048@gmail.com"],
        "subject": "✅ Test TrustDriver - Resend",
        "html": "<p>Félicitations ! Ton serveur Django peut envoyer des emails avec <strong>Resend</strong>.</p>"
    }
    
    email = resend.Emails.send(params)
    
    print(f"\n✅ Email envoyé avec succès !")
    print(f"Email ID: {email.get('id', 'N/A')}")
    print(f"\nVérifie ta boîte mail : edulms048@gmail.com")
    
except ImportError:
    print("\n❌ La bibliothèque 'resend' n'est pas installée")
    print("\nInstalle-la avec :")
    print("  pip install resend")
    
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    print("\nVérifie :")
    print("  • Que RESEND_API_KEY est correct")
    print("  • Que tu as une connexion internet")
    
    import traceback
    traceback.print_exc()
