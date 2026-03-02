#!/usr/bin/env python
"""
Script interactif pour configurer l'email Gmail dans Django
Usage: python backend/scripts/setup_email.py
"""
import os
from pathlib import Path

def main():
    print("=" * 70)
    print("🔧 CONFIGURATION EMAIL GMAIL POUR TRUSTDRIVER")
    print("=" * 70)
    
    backend_dir = Path(__file__).resolve().parent.parent
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        print(f"\n❌ Fichier {env_file} introuvable")
        print("Copie d'abord .env.example vers .env")
        return
    
    print("\n📋 ÉTAPES À SUIVRE :")
    print("\n1. Va sur : https://myaccount.google.com/apppasswords")
    print("2. Clique sur 'Sélectionner une application'")
    print("3. Choisis 'Autre (nom personnalisé)'")
    print("4. Tape : Django TrustDriver")
    print("5. Clique sur 'Générer'")
    print("6. Google va afficher un mot de passe à 16 caractères")
    print("\n" + "=" * 70)
    
    print("\n⚠️  IMPORTANT : Enlève TOUS les espaces du mot de passe !")
    print("   Si Google donne : 'abcd efgh ijkl mnop'")
    print("   Tu dois taper   : 'abcdefghijklmnop'")
    print("\n" + "=" * 70)
    
    app_password = input("\n🔑 Colle ton App Password Gmail (sans espaces) : ").strip()
    
    if not app_password:
        print("\n❌ Mot de passe vide. Annulation.")
        return
    
    if " " in app_password:
        print("\n⚠️  Attention : Le mot de passe contient des espaces.")
        remove_spaces = input("Voulez-vous les enlever automatiquement ? (o/n) : ").strip().lower()
        if remove_spaces == "o":
            app_password = app_password.replace(" ", "")
            print(f"✅ Espaces enlevés : {app_password}")
    
    if len(app_password) != 16:
        print(f"\n⚠️  Attention : Le mot de passe fait {len(app_password)} caractères (attendu : 16)")
        confirm = input("Continuer quand même ? (o/n) : ").strip().lower()
        if confirm != "o":
            print("Annulation.")
            return
    
    # Lire le fichier .env
    env_content = env_file.read_text(encoding="utf-8")
    
    # Remplacer EMAIL_HOST_PASSWORD
    lines = []
    password_updated = False
    
    for line in env_content.splitlines():
        if line.startswith("EMAIL_HOST_PASSWORD="):
            lines.append(f'EMAIL_HOST_PASSWORD="{app_password}"')
            password_updated = True
        else:
            lines.append(line)
    
    if not password_updated:
        # Ajouter la ligne si elle n'existe pas
        lines.append(f'EMAIL_HOST_PASSWORD="{app_password}"')
    
    # Écrire le fichier
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    print("\n✅ Fichier .env mis à jour avec succès !")
    print("\n" + "=" * 70)
    print("🧪 TEST DE LA CONFIGURATION")
    print("=" * 70)
    
    test_now = input("\nVoulez-vous tester l'envoi d'email maintenant ? (o/n) : ").strip().lower()
    
    if test_now == "o":
        print("\n📧 Test en cours...\n")
        os.system("python backend/scripts/test_email.py")
    else:
        print("\n💡 Pour tester plus tard, lance :")
        print("   npm run test:email")
        print("   ou")
        print("   python backend/scripts/test_email.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Annulé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
