# 🚀 Solution : Utiliser Resend avec le domaine par défaut

## ❌ Problème actuel

Render bloque les connexions SMTP sortantes (ports 587 et 465), donc Gmail SMTP ne fonctionne pas :
```
OSError: [Errno 101] Network is unreachable
```

## ✅ Solution : Resend avec domaine par défaut

Resend fournit un domaine gratuit `onboarding@resend.dev` qui fonctionne immédiatement.

---

## 📋 Configuration sur Render

### Étape 1 : Obtenir une clé API Resend

1. Va sur https://resend.com
2. Crée un compte (gratuit)
3. Va dans **API Keys**
4. Clique sur **Create API Key**
5. Donne-lui un nom : `TrustDriver Production`
6. Copie la clé (commence par `re_...`)

### Étape 2 : Configurer les variables sur Render

Sur ton dashboard Render, dans **Environment**, configure :

```
RESEND_API_KEY
re_VotreCléIci

RESEND_FROM_EMAIL
TrustDriver <onboarding@resend.dev>

DEFAULT_FROM_EMAIL
TrustDriver <onboarding@resend.dev>

FRONTEND_APP_URL
https://trustdriver.vercel.app
```

**IMPORTANT** : Supprime ou vide ces variables si elles existent :
```
EMAIL_HOST_PASSWORD
EMAIL_HOST_USER
EMAIL_USE_TLS
EMAIL_PORT
```

### Étape 3 : Redémarrer

Clique sur **Manual Deploy** ou **Restart Service**.

---

## 🎯 Pourquoi cette solution ?

### Avantages de Resend
- ✅ Fonctionne sur Render (pas de blocage réseau)
- ✅ 3000 emails/mois gratuits
- ✅ Meilleure délivrabilité que Gmail
- ✅ Analytics intégrés
- ✅ Pas de configuration DNS nécessaire avec `onboarding@resend.dev`

### Limites de Gmail SMTP sur Render
- ❌ Ports SMTP bloqués par Render
- ❌ 500 emails/jour maximum
- ❌ Peut être marqué comme spam
- ❌ Pas adapté pour la production

---

## 📧 Ce que les utilisateurs verront

**De** : `TrustDriver <onboarding@resend.dev>`  
**Sujet** : `Verify your TrustDriver email`

C'est professionnel et fonctionne parfaitement. Plus tard, tu pourras configurer un domaine personnalisé.

---

## 🔄 Alternative : Domaine personnalisé (optionnel)

Si tu as un domaine (ex: `trustdriver.com`) :

1. Va sur https://resend.com/domains
2. Clique sur **Add Domain**
3. Entre ton domaine : `trustdriver.com`
4. Configure les DNS records (SPF, DKIM, DMARC)
5. Attends la vérification (quelques minutes)
6. Utilise : `RESEND_FROM_EMAIL=TrustDriver <noreply@trustdriver.com>`

---

## 🧪 Test après configuration

1. Redémarre le service Render
2. Va sur https://trustdriver.vercel.app
3. Inscris-toi avec un nouvel email
4. Vérifie ta boîte mail (et spam)
5. Tu devrais recevoir l'email de vérification !

---

## 📊 Comparaison des solutions

| Solution | Fonctionne sur Render | Gratuit | Délivrabilité | Setup |
|----------|----------------------|---------|---------------|-------|
| Gmail SMTP | ❌ Non (bloqué) | ✅ Oui | ⚠️ Moyenne | Facile |
| Resend (défaut) | ✅ Oui | ✅ Oui (3k/mois) | ✅ Excellente | Très facile |
| Resend (domaine perso) | ✅ Oui | ✅ Oui (3k/mois) | ✅ Excellente | Moyen |

---

## 💡 Recommandation

**Pour l'instant** : Utilise Resend avec `onboarding@resend.dev`
- Configuration en 5 minutes
- Fonctionne immédiatement
- Gratuit jusqu'à 3000 emails/mois

**Plus tard** : Configure un domaine personnalisé
- Plus professionnel
- Meilleure confiance des utilisateurs
- Évite le dossier spam

---

## 🆘 Besoin d'aide ?

Si tu n'as pas encore de compte Resend :
1. Va sur https://resend.com
2. Clique sur **Sign Up**
3. Utilise ton email GitHub ou Google
4. C'est gratuit, pas de carte bancaire requise
