# ⚡ FIX RAPIDE - Email sur Render

## 🚨 Problème
```
OSError: [Errno 101] Network is unreachable
```
Render bloque les connexions SMTP (Gmail ne fonctionne pas).

---

## ✅ Solution en 5 minutes : Resend

### 1️⃣ Obtenir une clé API Resend (2 min)

1. Va sur **https://resend.com**
2. Clique sur **Sign Up** (gratuit, pas de CB)
3. Connecte-toi avec GitHub ou Google
4. Va dans **API Keys** (menu de gauche)
5. Clique sur **Create API Key**
6. Nom : `TrustDriver`
7. **Copie la clé** (commence par `re_...`)

### 2️⃣ Configurer Render (2 min)

1. Va sur **https://dashboard.render.com**
2. Sélectionne ton service backend
3. Clique sur **Environment**
4. Ajoute ces 2 variables :

```
RESEND_API_KEY
re_VotreCléCopiéeIci

RESEND_FROM_EMAIL
TrustDriver <onboarding@resend.dev>
```

5. Clique sur **Save Changes**

### 3️⃣ Redémarrer (1 min)

Le service redémarre automatiquement après la sauvegarde.

### 4️⃣ Tester

Va sur **https://trustdriver.vercel.app** et inscris-toi !

---

## 📧 Résultat

Les emails seront envoyés depuis :
```
TrustDriver <onboarding@resend.dev>
```

C'est le domaine par défaut de Resend, gratuit et sans configuration DNS.

---

## 💰 Limites gratuites

- **3000 emails/mois** gratuits
- Largement suffisant pour commencer
- Pas de carte bancaire requise

---

## 🎯 Pourquoi pas Gmail ?

Render bloque les ports SMTP (587, 465) pour éviter le spam.
Gmail SMTP ne fonctionnera jamais sur Render.

---

## ✨ Bonus : Domaine personnalisé (plus tard)

Quand tu auras un domaine (ex: `trustdriver.com`) :

1. Va sur https://resend.com/domains
2. Ajoute ton domaine
3. Configure les DNS
4. Change `RESEND_FROM_EMAIL` en `noreply@trustdriver.com`

Mais pour l'instant, `onboarding@resend.dev` fonctionne parfaitement !
