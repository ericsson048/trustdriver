# Backend Deploy

Ce dossier est autonome pour un deploiement backend Django.

## Fichiers principaux

- `manage.py`
- `requirements.txt`
- `.env.example`
- `build.sh`
- `start.sh`
- `config/`
- `apps/`

## Variables d'environnement

Copier :

`backend/.env.example` vers `backend/.env`

Variables principales :

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `FRONTEND_APP_URL`
- `DATABASE_URL`
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `DEFAULT_FROM_EMAIL`

En production, definir `DJANGO_DEBUG=false`. Le frontend Vercel appelle l'API Render sur un autre domaine, donc les cookies de session doivent etre emis avec `SameSite=None`, ce que Django ne fait pas quand `DEBUG=true`.

La verification email utilise `FRONTEND_APP_URL` pour construire le lien clique par l'utilisateur. En local, vous pouvez garder `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` pour afficher le lien de verification dans les logs. En production, configurez un vrai fournisseur SMTP.

## Render

Si le `Root Directory` du service Render est `backend`, utiliser :

- Build Command : `bash build.sh`
- Start Command : `bash start.sh`

Le backend utilisera :

- `backend/backend.sqlite3` si `DATABASE_URL` n'est pas defini
- `backend/media/` pour les uploads
- `backend/staticfiles/` pour les fichiers statiques collectes
