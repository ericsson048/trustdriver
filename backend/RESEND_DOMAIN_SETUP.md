# 🔓 Débloquer Resend pour envoyer à tous les emails

## ❌ Problème actuel

```
You can only send testing emails to your own email address (edulms048@gmail.com)
```

Resend en mode test ne permet d'envoyer qu'à ton email vérifié.

---

## ✅ Solution 1 : Vérifier ton email (2 minutes)

### Étape 1 : Vérifier ton email sur Resend

1. Va sur **https://resend.com/settings/emails**
2. Tu devrais voir ton email : `edulms048@gmail.com`
3. Clique sur **Verify** ou **Resend verification email**
4. Vérifie ta boîte mail et clique sur le lien
5. Une fois vérifié, tu pourras envoyer à d'autres adresses

⚠️ **Note** : Même avec l'email vérifié, Resend gratuit peut avoir des limitations. La vraie solution est d'ajouter un domaine.

---

## ✅ Solution 2 : Ajouter un domaine (si tu en as un)

Si tu as un domaine (ex: `trustdriver.com`, `monsite.fr`, etc.) :

### Étape 1 : Ajouter le domaine sur Resend

1. Va sur **https://resend.com/domains**
2. Clique sur **Add Domain**
3. Entre ton domaine : `trustdriver.com`
4. Resend va te donner des records DNS à configurer

### Étape 2 : Configurer les DNS

Chez ton hébergeur DNS (Cloudflare, Namecheap, etc.), ajoute ces records :

**SPF Record (TXT)**
```
Type: TXT
Name: @
Value: v=spf1 include:_spf.resend.com ~all
```

**DKIM Record (TXT)**
```
Type: TXT
Name: resend._domainkey
Value: [fourni par Resend]
```

**DMARC Record (TXT)** (optionnel mais recommandé)
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@trustdriver.com
```

### Étape 3 : Vérifier le domaine

1. Retourne sur Resend
2. Clique sur **Verify Domain**
3. Attends quelques minutes (propagation DNS)
4. Une fois vérifié, tu verras un ✅ vert

### Étape 4 : Mettre à jour Render

Sur Render, change :
```
RESEND_FROM_EMAIL=TrustDriver <noreply@trustdriver.com>
```

---

## ✅ Solution 3 : Utiliser Brevo (RECOMMANDÉ si pas de domaine)

Si tu n'as pas de domaine, Brevo est plus simple :
- 300 emails/jour gratuits
- Pas de restriction de destinataire
- Pas besoin de domaine

Voir `BREVO_SETUP.md` pour la configuration.

---

## 🎯 Quelle solution choisir ?

### Tu as un domaine ?
→ **Utilise Resend avec domaine vérifié**
- Meilleure délivrabilité
- Plus professionnel
- 3000 emails/mois gratuits

### Tu n'as PAS de domaine ?
→ **Utilise Brevo**
- Configuration en 5 minutes
- Fonctionne immédiatement
- 300 emails/jour gratuits

### Tu veux tester rapidement ?
→ **Utilise Brevo**
- Pas de configuration DNS
- Pas de domaine requis
- Fonctionne tout de suite

---

## 📝 Checklist

**Pour Resend avec domaine :**
- [ ] Acheter/avoir un domaine
- [ ] Ajouter le domaine sur Resend
- [ ] Configurer les DNS (SPF, DKIM)
- [ ] Vérifier le domaine
- [ ] Mettre à jour `RESEND_FROM_EMAIL` sur Render
- [ ] Tester l'inscription

**Pour Brevo (plus simple) :**
- [ ] Créer un compte Brevo
- [ ] Obtenir la clé SMTP
- [ ] Configurer les variables sur Render
- [ ] Supprimer `RESEND_API_KEY`
- [ ] Tester l'inscription

---

## 💰 Coût d'un domaine

Si tu veux acheter un domaine :
- **Namecheap** : ~10€/an
- **Google Domains** : ~12€/an
- **OVH** : ~8€/an
- **Cloudflare** : ~10€/an

Exemples de domaines :
- `trustdriver.com`
- `trustdriver.app`
- `trustdriver.io`

---

## 🚀 Ma recommandation

**Court terme (maintenant)** :
→ Utilise **Brevo** pour débloquer immédiatement

**Moyen terme (dans 1-2 semaines)** :
→ Achète un domaine et configure Resend

**Long terme (après lancement)** :
→ Garde Resend avec domaine personnalisé pour la meilleure délivrabilité
