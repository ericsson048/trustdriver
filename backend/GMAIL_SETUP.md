# Configuration Gmail pour Django

## ⚠️ SÉCURITÉ IMPORTANTE

**Ton ancien App Password a été exposé publiquement. Tu DOIS le révoquer immédiatement.**

## Étapes de configuration

### 1. Révoquer l'ancien mot de passe (URGENT)

1. Va sur https://myaccount.google.com/security
2. Clique sur "Mots de passe des applications"
3. Supprime le mot de passe existant pour Django/Mail

### 2. Générer un nouveau App Password

1. Sur la même page, clique sur "Créer"
2. Choisis :
   - **App** : Mail
   - **Device** : Other (Django)
3. Google va générer un mot de passe à 16 caractères (ex: `abcd efgh ijkl mnop`)
4. **Copie-le immédiatement** (tu ne pourras plus le revoir)

### 3. Mettre à jour backend/.env

```env
EMAIL_HOST_USER="edulms048@gmail.com"
EMAIL_HOST_PASSWORD="ton nouveau app password ici"
EMAIL_USE_TLS="true"
DEFAULT_FROM_EMAIL="TrustDriver <edulms048@gmail.com>"
```

### 4. Tester l'envoi d'email

```bash
cd backend
python manage.py shell < scripts/test_email.py
```

Ou en mode interactif :

```bash
python manage.py shell
```

Puis dans le shell :

```python
from django.core.mail import send_mail

send_mail(
    subject="Test TrustDriver",
    message="Email de test",
    from_email="edulms048@gmail.com",
    recipient_list=["edulms048@gmail.com"],
    fail_silently=False,
)
```

## Erreurs courantes

### 535 Incorrect authentication data

**Cause** : Mauvais App Password ou 2FA non activé

**Solution** :
- Vérifie que la 2FA est activée sur ton compte Google
- Génère un nouveau App Password
- Copie-le EXACTEMENT (sans espaces)

### Connection refused / Timeout

**Cause** : Port 587 bloqué par firewall/proxy

**Solution** :
- Essaie le port 465 avec `EMAIL_USE_SSL=True` au lieu de `EMAIL_USE_TLS`
- Vérifie ton firewall/antivirus

### SMTPAuthenticationError

**Cause** : Tu utilises ton mot de passe Gmail normal au lieu d'un App Password

**Solution** :
- Ne JAMAIS utiliser ton mot de passe Gmail principal
- Toujours utiliser un App Password

## Configuration pour production (Render)

Sur Render, ajoute ces variables d'environnement :

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=edulms048@gmail.com
EMAIL_HOST_PASSWORD=ton_app_password
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=TrustDriver <edulms048@gmail.com>
```

## Alternative : Resend (recommandé pour production)

Gmail gratuit a des limites (500 emails/jour). Pour la production, utilise Resend :

1. Crée un compte sur https://resend.com
2. Obtiens une API key
3. Configure dans `.env` :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=ta_resend_api_key
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=TrustDriver <onboarding@resend.dev>
```

## Vérification de la configuration actuelle

```python
from django.conf import settings

print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
```
