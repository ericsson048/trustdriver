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
- `DATABASE_URL`

En production, definir `DJANGO_DEBUG=false`. Le frontend Vercel appelle l'API Render sur un autre domaine, donc les cookies de session doivent etre emis avec `SameSite=None`, ce que Django ne fait pas quand `DEBUG=true`.

## Render

Si le `Root Directory` du service Render est `backend`, utiliser :

- Build Command : `bash build.sh`
- Start Command : `bash start.sh`

Le backend utilisera :

- `backend/backend.sqlite3` si `DATABASE_URL` n'est pas defini
- `backend/media/` pour les uploads
- `backend/staticfiles/` pour les fichiers statiques collectes
