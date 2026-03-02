---
inclusion: always
---

# Tech Stack

## Frontend
- React 19 with TypeScript
- Vite 6 as build tool
- Tailwind CSS 4 for styling
- Lucide React for icons
- Motion for animations
- Additional libraries: date-fns, dompurify, jszip, mammoth, xlsx

## Backend
- Django 5.1+ with Python 3.12+
- Django REST Framework for API
- drf-spectacular for OpenAPI/Swagger docs
- Gunicorn as WSGI server
- PostgreSQL (production) or SQLite (development)

## Build System
- Frontend: Vite with TypeScript compiler
- Backend: Python with pip/requirements.txt
- Path alias: `@/` resolves to project root

## Common Commands

Development:
```bash
npm run dev              # Start Vite dev server (port 5173)
npm run dev:backend      # Start Django server (port 8000)
npm run dev:frontend     # Alias for npm run dev
```

Build & Deploy:
```bash
npm run build            # TypeScript compile + Vite build
npm run preview          # Preview production build
npm run clean            # Remove dist folder
```

Backend:
```bash
npm run migrate          # Apply Django migrations
npm run createsuperuser  # Create Django admin user
npm run serve:backend    # Run Django server
npm run test:api         # Run API flow tests
```

Linting:
```bash
npm run lint             # TypeScript type checking (no emit)
```

## Environment Files
- `.env` - Frontend Vite variables
- `.env.production` - Frontend production build
- `backend/.env` - Django backend variables

## Development Proxy
Vite proxies `/api` and `/media` to `http://127.0.0.1:8000` in development.

## Deployment
- Frontend: Vercel (uses `/` base path)
- Backend: Render (uses `/static/` base path for serving frontend)
- Production backend: `https://trustdriver.onrender.com`
- Production frontend: `https://trustdriver.vercel.app`
