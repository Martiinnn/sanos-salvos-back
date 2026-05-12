# Deploy Guide

## 1) Backend on Render

### Prerequisites
- Repository connected to Render.
- `render.yaml` exists at repo root.

### Deploy
1. In Render Dashboard, click **New +** -> **Blueprint**.
2. Select this repository and branch (`master` recommended for production).
3. Confirm all services from `render.yaml`:
   - `sys-postgres`
   - `sys-rabbitmq`
   - `sys-pets`
   - `sys-geo`
   - `sys-match`
   - `sys-notifications`
   - `sys-gateway` (public entrypoint)
4. Start deploy.

### Initialize DB schemas/tables
After Postgres is created, run `init-db.sql` once against `sys-postgres`:
- Open Render Postgres shell/connection.
- Execute the SQL content from [`init-db.sql`](./init-db.sql).

> Without this step, auth and report tables will be missing.

## 2) Frontend on Firebase Hosting

### Prerequisites
- Firebase project with Authentication enabled.
- `Email/Password` and `Google` providers enabled (if used).
- Authorized domains include `localhost`, `127.0.0.1`, and your Firebase Hosting domain.

### Frontend env for production
Create `frontend/.env.production` using [`frontend/.env.production.example`](./frontend/.env.production.example):

- Set `VITE_API_BASE` to your Render gateway URL, e.g.:
  - `https://sys-gateway.onrender.com/api`
- Fill Firebase keys.

### Deploy commands
From `frontend/`:

```bash
npm install
npm run build
npx firebase login
npx firebase init hosting
npx firebase deploy --only hosting
```

Use:
- public directory: `dist`
- single-page app rewrite: `yes`

## 3) End-to-end smoke test

1. Open Firebase Hosting URL.
2. Register with email/password.
3. Login with email/password and Google.
4. Create report through gateway.
5. Check matches/notifications flow.
