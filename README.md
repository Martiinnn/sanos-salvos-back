# Sanos y Salvos - Backend

Backend de la plataforma Sanos y Salvos para reportar mascotas perdidas/encontradas,
geolocalizar reportes y gestionar coincidencias.

## Production

- Frontend (Firebase Hosting): https://sanosysalvos-f9906.web.app/
- Backend (Render): API Gateway + microservicios FastAPI

## Current Architecture

- API Gateway (`gateway`)
- Pets Service (`services/pets`)
- Geolocation Service (`services/geolocation`)
- Match Service (`services/match`)
- Notifications Service (`services/notifications`)
- Shared Postgres database (Neon)

Important:
- RabbitMQ was removed.
- Service-to-service communication is HTTP via Gateway routing/proxy.
- Frontend auth is handled with Firebase Auth.

## API Entry Point

- Local: `http://localhost:8000`
- Render: `https://<your-gateway>.onrender.com`

Main routed prefixes:
- `/api/pets/*`
- `/api/geo/*`
- `/api/matches/*`
- `/api/notifications/*`

Gateway auth endpoints:
- `/api/auth/register`
- `/api/auth/login`
- `/api/auth/me`

## Required Environment Variables

### Shared (gateway and DB-backed services)

```env
POSTGRES_HOST=
POSTGRES_PORT=5432
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

### Gateway

```env
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

PETS_SERVICE_HOST=
PETS_SERVICE_PORT=
GEO_SERVICE_HOST=
GEO_SERVICE_PORT=
MATCH_SERVICE_HOST=
MATCH_SERVICE_PORT=
NOTIFICATIONS_SERVICE_HOST=
NOTIFICATIONS_SERVICE_PORT=
```

## Local Run (without Docker)

Run each service in its folder:

```bash
# Example
cd gateway
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Do the same for:
- `services/pets` (port 8001)
- `services/geolocation` (port 8002)
- `services/match` (port 8003)
- `services/notifications` (port 8004)

## Database Setup

Before creating reports, ensure schemas/tables exist in Postgres.
At minimum, create schemas used by services:

- `auth_service`
- `pets_service`
- `geo_service`
- `match_service`
- `notifications_service`

Then execute your SQL initialization script (`init-db.sql`) against the same database.

## Notes

- Notifications service currently stores notifications in memory (demo mode).
- Render free instances can sleep on inactivity and take time to wake up.
