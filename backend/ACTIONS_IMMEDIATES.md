# 🚨 ACTIONS IMMÉDIATES - SÉCURITÉ

## ⚠️ TON APP PASSWORD GMAIL A ÉTÉ EXPOSÉ

Tu as partagé publiquement : `ifgq wumr wapv ltmj`

### Action 1 : RÉVOQUER IMMÉDIATEMENT (5 minutes)

1. Va sur https://myaccount.google.com/security
2. Clique sur **"Mots de passe des applications"**
3. **SUPPRIME** le mot de passe existant
4. Génère un **NOUVEAU** App Password
5. Mets-le dans `backend/.env` (ligne `EMAIL_HOST_PASSWORD`)

### Action 2 : Tester la nouvelle configuration

```bash
cd backend
python scripts/test_email.py
```

Si tu vois "✅ Email envoyé avec succès", c'est bon !

### Action 3 : Mettre à jour Render (production)

Sur ton dashboard Render :

1. Va dans **Environment**
2. Mets à jour `EMAIL_HOST_PASSWORD` avec le nouveau mot de passe
3. Redémarre le service

---

## 📋 CHECKLIST DE CONFIGURATION

### Gmail (gratuit, 500 emails/jour)

- [ ] 2FA activé sur compte Google
- [ ] App Password généré
- [ ] `EMAIL_HOST_PASSWORD` mis à jour dans `.env`
- [ ] Test d'envoi réussi
- [ ] Variables mises à jour sur Render

### Configuration actuelle dans backend/.env

```env
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
EMAIL_HOST_USER="edulms048@gmail.com"
EMAIL_HOST_PASSWORD="YOUR_NEW_APP_PASSWORD_HERE"  # ← CHANGE MOI
EMAIL_USE_TLS="true"
DEFAULT_FROM_EMAIL="TrustDriver <edulms048@gmail.com>"
```

---

## 🧪 TESTS RAPIDES

### Test 1 : Configuration Django

```bash
cd backend
python manage.py shell
```

```python
from django.conf import settings
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
print(f"Backend: {settings.EMAIL_BACKEND}")
```

### Test 2 : Envoi d'email simple

```python
from django.core.mail import send_mail

send_mail(
    subject="Test TrustDriver",
    message="Si tu reçois cet email, ça marche !",
    from_email="edulms048@gmail.com",
    recipient_list=["edulms048@gmail.com"],
    fail_silently=False,
)
```

### Test 3 : Email de vérification complet

```python
from apps.accounts.models import User, EmailVerificationToken

# Crée un utilisateur test
user = User.objects.create_user(
    email="test@example.com",
    password="testpass123"
)

# Génère et envoie le token
token = EmailVerificationToken.objects.create(user=user)
token.send_verification_email()

print(f"Token généré : {token.token}")
```

---

## 🔧 DÉPANNAGE

### Erreur : 535 Authentication failed

**Cause** : Mauvais App Password

**Solution** :
1. Vérifie que tu as copié le mot de passe EXACTEMENT (sans espaces)
2. Vérifie que la 2FA est activée
3. Génère un nouveau App Password si besoin

### Erreur : Connection refused

**Cause** : Port 587 bloqué

**Solution** : Essaie avec port 465 et SSL

```env
EMAIL_PORT="465"
EMAIL_USE_TLS="false"
EMAIL_USE_SSL="true"
```

### Emails vont dans spam

**Solution** :
- Utilise un domaine personnalisé (pas @gmail.com)
- Configure SPF/DKIM records
- Ou utilise Resend pour production

---

## 🚀 ALTERNATIVE : RESEND (RECOMMANDÉ POUR PRODUCTION)

Gmail gratuit = 500 emails/jour max. Pour production, utilise Resend :

### Avantages Resend
- 3000 emails/mois gratuits
- Meilleure délivrabilité
- Analytics intégrés
- Pas de limite quotidienne stricte

### Configuration Resend

1. Crée un compte sur https://resend.com
2. Obtiens une API key
3. Mets à jour `backend/.env` :

```env
RESEND_API_KEY="re_VotreCléIci"
RESEND_FROM_EMAIL="TrustDriver <onboarding@resend.dev>"
```

Le code dans `emailing.py` détecte automatiquement Resend et l'utilise en priorité.

---

## 📝 NOTES IMPORTANTES

1. **Ne JAMAIS commit** les fichiers `.env` dans Git
2. **Toujours utiliser** des App Passwords, jamais ton mot de passe Gmail principal
3. **Révoquer immédiatement** tout mot de passe exposé
4. **Utiliser Resend** pour la production (meilleure délivrabilité)

---

## ✅ PROCHAINES ÉTAPES

1. [ ] Révoquer l'ancien App Password
2. [ ] Générer un nouveau App Password
3. [ ] Tester avec `python scripts/test_email.py`
4. [ ] Mettre à jour les variables sur Render
5. [ ] Tester l'inscription d'un nouvel utilisateur
6. [ ] (Optionnel) Migrer vers Resend pour production
