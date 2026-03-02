# 🚀 Configuration Email sur Render

## ❌ Problème actuel

```
EmailDeliveryError: Resend API error: 
{"statusCode":403,"message":"The gmail.com domain is not verified"}
```

**Cause** : Render utilise Resend au lieu de Gmail SMTP car `RESEND_API_KEY` est configuré.

---

## ✅ Solution : Utiliser Gmail SMTP sur Render

### Étape 1 : Accéder aux variables d'environnement

1. Va sur https://dashboard.render.com
2. Clique sur ton service backend : **trustdriver**
3. Dans le menu de gauche, clique sur **Environment**

### Étape 2 : Supprimer/Vider RESEND_API_KEY

Trouve la variable `RESEND_API_KEY` et :
- Soit **supprime-la** complètement (bouton poubelle)
- Soit mets une valeur vide : `""`

### Étape 3 : Configurer Gmail SMTP

Ajoute ou mets à jour ces variables :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=edulms048@gmail.com
EMAIL_HOST_PASSWORD=sbkfywfbtywkbera
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=TrustDriver <edulms048@gmail.com>
FRONTEND_APP_URL=https://trustdriver.vercel.app
```

⚠️ **Important** : Utilise le même App Password que tu as généré pour le développement local.

### Étape 4 : Redémarrer le service

1. En haut à droite, clique sur **Manual Deploy**
2. Ou clique sur **Restart Service**
3. Attends que le service redémarre (1-2 minutes)

### Étape 5 : Tester

Une fois redémarré, teste l'inscription depuis le frontend :
- https://trustdriver.vercel.app

Tu devrais recevoir l'email de vérification !

---

## 🔍 Vérification des variables

Voici toutes les variables d'environnement nécessaires sur Render :

### Variables obligatoires

```env
# Django
DJANGO_SECRET_KEY=ton_secret_key_production
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=trustdriver.onrender.com
FRONTEND_APP_URL=https://trustdriver.vercel.app

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://...

# Email (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=edulms048@gmail.com
EMAIL_HOST_PASSWORD=sbkfywfbtywkbera
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=TrustDriver <edulms048@gmail.com>
```

### Variables à NE PAS mettre (ou vider)

```env
RESEND_API_KEY=    # ← Vide ou supprimé
RESEND_FROM_EMAIL= # ← Vide ou supprimé
```

---

## 🎯 Logique de sélection Email

Le code dans `emailing.py` fonctionne ainsi :

```python
def send_email_message(...):
    if settings.RESEND_API_KEY:  # ← Si cette variable existe
        send_with_resend(...)     # ← Utilise Resend
        return
    
    send_mail(...)                # ← Sinon utilise Django SMTP (Gmail)
```

Donc pour utiliser Gmail SMTP, il faut que `RESEND_API_KEY` soit :
- Absente
- Vide (`""`)
- Ou `None`

---

## 🚀 Alternative : Utiliser Resend (recommandé pour production)

Gmail gratuit a des limites :
- 500 emails/jour maximum
- Peut être bloqué par certains FAI
- Moins bonne délivrabilité

Pour la production, Resend est meilleur :

### Avantages Resend
- 3000 emails/mois gratuits
- Meilleure délivrabilité
- Analytics intégrés
- Support des domaines personnalisés

### Configuration Resend

1. **Crée un compte** sur https://resend.com

2. **Obtiens une API key** :
   - Va dans Settings → API Keys
   - Crée une nouvelle clé
   - Copie-la

3. **Configure sur Render** :
   ```env
   RESEND_API_KEY=re_VotreCléIci
   RESEND_FROM_EMAIL=TrustDriver <onboarding@resend.dev>
   ```

4. **Option : Domaine personnalisé** (recommandé)
   - Va sur https://resend.com/domains
   - Ajoute ton domaine (ex: trustdriver.com)
   - Configure les DNS records (SPF, DKIM)
   - Utilise : `RESEND_FROM_EMAIL=TrustDriver <noreply@trustdriver.com>`

---

## 🧪 Test après configuration

### Test 1 : Vérifier les logs Render

Dans les logs Render, tu ne devrais plus voir :
```
Resend API error: {"statusCode":403...
```

### Test 2 : Inscription d'un utilisateur

1. Va sur https://trustdriver.vercel.app
2. Inscris-toi avec un nouvel email
3. Vérifie que tu reçois l'email de vérification

### Test 3 : Vérifier l'email reçu

L'email devrait venir de :
- **Avec Gmail** : `edulms048@gmail.com` ou `TrustDriver <edulms048@gmail.com>`
- **Avec Resend** : `onboarding@resend.dev` ou ton domaine personnalisé

---

## 📝 Checklist de déploiement

- [ ] `RESEND_API_KEY` supprimé ou vidé sur Render
- [ ] `EMAIL_HOST_PASSWORD` configuré avec l'App Password Gmail
- [ ] `EMAIL_USE_TLS=true` configuré
- [ ] `FRONTEND_APP_URL=https://trustdriver.vercel.app` configuré
- [ ] Service Render redémarré
- [ ] Test d'inscription réussi
- [ ] Email de vérification reçu

---

## 🆘 Dépannage

### Erreur : "Username and Password not accepted"

**Cause** : App Password Gmail incorrect

**Solution** :
- Vérifie que tu as copié le bon App Password
- Génère un nouveau App Password si besoin
- Mets à jour `EMAIL_HOST_PASSWORD` sur Render

### Erreur : "Connection refused"

**Cause** : Port 587 bloqué par Render

**Solution** : Essaie le port 465 avec SSL
```env
EMAIL_PORT=465
EMAIL_USE_TLS=false
EMAIL_USE_SSL=true
```

Puis ajoute dans `settings.py` :
```python
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
```

### Emails vont dans spam

**Solution** :
- Utilise Resend avec un domaine personnalisé
- Configure SPF/DKIM records
- Utilise un domaine professionnel (pas @gmail.com)

---

## 💡 Recommandation finale

**Pour l'instant (développement/test)** :
- Utilise Gmail SMTP (gratuit, facile)

**Pour la production (après lancement)** :
- Migre vers Resend avec domaine personnalisé
- Meilleure délivrabilité et professionnalisme
- Analytics et monitoring intégrés
