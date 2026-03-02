# 📧 Configuration Brevo (ex-Sendinblue) - Alternative à Resend

## ❌ Problème avec Resend

Resend gratuit ne permet d'envoyer qu'à ton propre email vérifié, ce qui bloque les inscriptions d'utilisateurs.

## ✅ Solution : Brevo (300 emails/jour gratuits)

Brevo (anciennement Sendinblue) offre :
- 300 emails/jour gratuits
- Pas de restriction de destinataire
- Pas besoin de domaine personnalisé
- Configuration SMTP simple

---

## 📋 Configuration Brevo (5 minutes)

### Étape 1 : Créer un compte Brevo

1. Va sur **https://www.brevo.com**
2. Clique sur **Sign Up Free**
3. Inscris-toi avec ton email
4. Vérifie ton email

### Étape 2 : Obtenir les identifiants SMTP

1. Connecte-toi à Brevo
2. Va dans **Settings** (en haut à droite)
3. Clique sur **SMTP & API**
4. Dans la section **SMTP**, tu verras :
   - **SMTP Server** : `smtp-relay.brevo.com`
   - **Port** : `587`
   - **Login** : ton email
   - **SMTP Key** : Clique sur **Create a new SMTP key**

5. Copie la clé SMTP générée

### Étape 3 : Configurer sur Render

Sur ton dashboard Render, dans **Environment**, configure :

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=ton_email@gmail.com
EMAIL_HOST_PASSWORD=ta_cle_smtp_brevo
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=TrustDriver <ton_email@gmail.com>
FRONTEND_APP_URL=https://trustdriver.vercel.app
```

**IMPORTANT** : Supprime ou vide ces variables :
```
RESEND_API_KEY
RESEND_FROM_EMAIL
```

### Étape 4 : Redémarrer

Le service redémarre automatiquement après la sauvegarde.

---

## 🎯 Avantages de Brevo

| Critère | Resend (gratuit) | Brevo (gratuit) |
|---------|------------------|-----------------|
| Emails/jour | 100 | 300 |
| Restriction destinataire | ❌ Oui (email vérifié uniquement) | ✅ Non |
| Domaine requis | ⚠️ Recommandé | ❌ Non |
| SMTP | ❌ Non (API uniquement) | ✅ Oui |
| Setup | Moyen | Facile |

---

## 🧪 Test après configuration

1. Redémarre le service Render
2. Va sur https://trustdriver.vercel.app
3. Inscris-toi avec N'IMPORTE QUEL email
4. Tu devrais recevoir l'email de vérification !

---

## 📊 Comparaison complète

### Resend
- ✅ 3000 emails/mois
- ❌ Domaine requis pour production
- ❌ Restriction en mode test
- ✅ Bonne délivrabilité

### Brevo
- ✅ 300 emails/jour (9000/mois)
- ✅ Pas de domaine requis
- ✅ Pas de restriction
- ✅ SMTP standard
- ✅ Dashboard avec analytics

### Gmail SMTP
- ❌ Bloqué sur Render
- ✅ 500 emails/jour
- ⚠️ Délivrabilité moyenne

---

## 💡 Recommandation

**Pour TrustDriver** : Utilise Brevo
- Gratuit et généreux
- Fonctionne immédiatement
- Pas de configuration DNS
- Parfait pour démarrer

**Plus tard** : Quand tu auras un domaine personnalisé, tu pourras migrer vers Resend avec domaine vérifié.

---

## 🆘 Alternative : Mailgun

Si Brevo ne te convient pas, Mailgun offre aussi un plan gratuit :
- 5000 emails/mois gratuits (3 premiers mois)
- Puis 1000 emails/mois gratuits
- Configuration SMTP similaire

https://www.mailgun.com
