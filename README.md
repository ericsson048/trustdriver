# TrustDriver

TrustDriver utilise maintenant :

- un frontend React + Vite dans `src/`
- un backend Django dans `backend/`
- une API maintenue sous les memes routes `/api/...`

## Prerequis

- Node.js
- Python 3.12+

## Installation

1. Installer les dependances frontend :
   `npm install`
2. Installer les dependances Python :
   `pip install -r requirements.txt`
3. Creer un fichier d'environnement a partir de l'exemple :
   `copy .env.example .env`
4. Appliquer les migrations :
   `npm run migrate`

Le backend peut utiliser PostgreSQL via `DATABASE_URL`. Si cette variable est definie, Django utilisera PostgreSQL a la place de SQLite.

## Lancement en developpement

1. Demarrer Django :
   `npm run dev:backend`
2. Dans un second terminal, demarrer Vite :
   `npm run dev`

Le serveur Vite proxifie automatiquement `/api` et `/media` vers `http://127.0.0.1:8000`.

## Structure backend

- `backend/config/` : configuration Django
- `backend/apps/accounts/` : utilisateur et authentification
- `backend/apps/drive/` : modeles, logique metier et endpoints fichiers

## Endpoints principaux

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/files`
- `POST /api/folders`
- `POST /api/upload`
- `GET /api/download/<id>`
- `DELETE /api/nodes/<id>`
- `POST /api/share/<id>`
- `GET /api/shared/<token>`
- `GET /api/shared/<token>/download`

## Documentation API

- Swagger UI : `http://127.0.0.1:8000/docs/swagger/`
- OpenAPI JSON : `http://127.0.0.1:8000/docs/openapi.json`
