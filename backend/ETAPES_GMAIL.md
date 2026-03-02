# 🔐 Générer un App Password Gmail - Guide Étape par Étape

## Prérequis
- Compte Gmail : edulms048@gmail.com
- Validation en 2 étapes ACTIVÉE (obligatoire)

---

## Étape 1 : Activer la validation en 2 étapes (si pas déjà fait)

1. Va sur : https://myaccount.google.com/security
2. Cherche "Validation en 2 étapes"
3. Clique sur "Activer"
4. Suis les instructions (SMS ou application Google Authenticator)

---

## Étape 2 : Générer un App Password

1. Va sur : https://myaccount.google.com/apppasswords
   
   OU
   
   - Va sur https://myaccount.google.com/security
   - Cherche "Mots de passe des applications"
   - Clique dessus

2. Tu verras une page "Mots de passe des applications"

3. Clique sur "Sélectionner une application"
   - Choisis : **Autre (nom personnalisé)**
   - Tape : **Django TrustDriver**

4. Clique sur "Générer"

5. Google va afficher un mot de passe à 16 caractères comme :
   ```
   abcd efgh ijkl mnop
   ```

6. **COPIE-LE IMMÉDIATEMENT** (tu ne pourras plus le revoir)

---

## Étape 3 : Mettre à jour backend/.env

Ouvre `backend/.env` et remplace cette ligne :

```env
EMAIL_HOST_PASSWORD="YOUR_NEW_APP_PASSWORD_HERE"
```

Par (SANS ESPACES) :

```env
EMAIL_HOST_PASSWORD="abcdefghijklmnop"
```

⚠️ **IMPORTANT** : Enlève tous les espaces du mot de passe !

Si Google te donne : `abcd efgh ijkl mnop`
Tu dois mettre : `abcdefghijklmnop`

---

## Étape 4 : Tester

```bash
npm run test:email
```

Ou :

```bash
cd backend
python scripts/test_email.py
```

---

## ❌ Erreurs courantes

### "Username and Password not accepted"

**Causes possibles :**
1. App Password incorrect (espaces non enlevés)
2. 2FA non activé
3. Ancien mot de passe Gmail utilisé (interdit)
4. App Password révoqué

**Solution :**
- Génère un NOUVEAU App Password
- Copie-le EXACTEMENT sans espaces
- Vérifie que la 2FA est activée

### "Connection refused"

**Cause :** Port 587 bloqué par firewall

**Solution :** Essaie le port 465 avec SSL

Dans `backend/.env` :
```env
EMAIL_PORT="465"
EMAIL_USE_TLS="false"
EMAIL_USE_SSL="true"
```

Puis ajoute dans `backend/config/settings.py` après `EMAIL_USE_TLS` :
```python
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
```

---

## ✅ Vérification rapide

Une fois configuré, teste dans le shell Django :

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject="✅ Test TrustDriver",
    message="Si tu reçois cet email, la configuration fonctionne !",
    from_email="edulms048@gmail.com",
    recipient_list=["edulms048@gmail.com"],
    fail_silently=False,
)
```

Si tu vois `1` (pas d'erreur), vérifie ta boîte mail !

---

## 🔒 Sécurité

- Ne JAMAIS partager ton App Password
- Ne JAMAIS commit le fichier `.env` dans Git
- Révoquer immédiatement tout App Password exposé
- Utiliser des App Passwords différents pour chaque application

---

## 📞 Besoin d'aide ?

Si ça ne marche toujours pas après avoir suivi ces étapes :

1. Vérifie que tu as bien copié le mot de passe SANS espaces
2. Vérifie que la 2FA est activée
3. Essaie de générer un nouveau App Password
4. Vérifie que ton compte Gmail n'a pas de restrictions
