---
inclusion: always
---

# Project Structure

## Root Layout
```
/                           # Monorepo root
├── src/                    # React frontend source
├── backend/                # Django backend (standalone deployable)
├── dist/                   # Vite build output
├── media/                  # User uploads (root level, legacy)
├── .env                    # Frontend environment
├── .env.production         # Frontend production env
├── package.json            # Frontend dependencies & scripts
├── vite.config.ts          # Vite configuration
└── tsconfig.json           # TypeScript configuration
```

## Frontend Structure (`src/`)
```
src/
├── components/             # React components
├── lib/                    # Utilities and configuration
│   └── apiConfig.ts        # Centralized API URLs
├── App.tsx                 # Main app component
├── main.tsx                # React entry point
├── types.ts                # TypeScript type definitions
└── index.css               # Global styles
```

## Backend Structure (`backend/`)
```
backend/
├── config/                 # Django project configuration
│   ├── settings.py         # Main settings (env-based config)
│   ├── urls.py             # Root URL routing
│   ├── middleware.py       # Custom middleware (CORS)
│   ├── wsgi.py             # WSGI entry
│   └── asgi.py             # ASGI entry
├── apps/                   # Django applications
│   ├── accounts/           # User authentication & email verification
│   ├── drive/              # File/folder models & endpoints
│   └── api_docs/           # Swagger/OpenAPI documentation
├── media/                  # User file uploads
│   └── uploads/            # Organized by user UUID
├── staticfiles/            # Collected static files (production)
├── scripts/                # Utility scripts
│   └── test_api_flow.py    # API testing script
├── manage.py               # Django management
├── requirements.txt        # Python dependencies
├── .env                    # Backend environment
├── build.sh                # Render build script
└── start.sh                # Render start script
```

## Django Apps Architecture

### accounts
- Custom User model (email-based auth)
- Email verification with tokens
- Session-based authentication
- Endpoints: register, login, logout, verify, resend-verification, me

### drive
- Node model (files and folders in tree structure)
- File upload/download
- Folder creation
- Sharing with secure tokens
- Endpoints: files, folders, upload, download, nodes, share, shared

### api_docs
- Swagger UI at `/docs/swagger/`
- OpenAPI JSON at `/docs/openapi.json`

## Key Conventions

- Django apps use `apps.` prefix in INSTALLED_APPS
- Custom User model: `accounts.User` (AUTH_USER_MODEL)
- API endpoints prefixed with `/api/`
- Media files served at `/media/`
- Static files at `/static/` (production)
- Frontend uses `@/` alias for imports (resolves to project root)
- Environment variables loaded via custom `load_env_file()` in settings
- Database: SQLite (dev) or PostgreSQL via DATABASE_URL (prod)
- CORS handled by custom SimpleCorsMiddleware
- Session cookies: SameSite=Lax (dev), SameSite=None (prod)

## File Organization Patterns

- Backend migrations in `apps/<app>/migrations/`
- User uploads in `backend/media/uploads/<user_uuid>/`
- Frontend build output in `dist/` (served by Django in production)
- TypeScript types centralized in `src/types.ts`
- API configuration centralized in `src/lib/apiConfig.ts`
