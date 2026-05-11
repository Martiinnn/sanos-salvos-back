# Run Without Docker

This project can run locally with:
- Python 3.11+
- Node.js 22+
- PostgreSQL running on `localhost:5432`

RabbitMQ is optional for the minimum demo (auth + gateway + pets); if it is not running, event publishing logs warnings but the core flow still works.

## 1) Create DB and tables (auth + pets)

From repo root:

```powershell
Get-Content .env.local | ForEach-Object {
  if ($_ -and -not $_.StartsWith("#")) {
    $k,$v = $_.Split("=",2)
    [System.Environment]::SetEnvironmentVariable($k,$v,"Process")
  }
}
python -m pip install psycopg2-binary
python .\scripts\init-local-db.py
```

## 2) Start frontend + gateway + pets

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-local.ps1
```

This opens three PowerShell windows:
- Pets service on `http://localhost:8001`
- Gateway on `http://localhost:8000`
- Frontend on `http://localhost:5173`

## 3) Validate minimum required flow

In a new terminal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-local-auth-flow.ps1
```

If successful, it verifies:
- User registration (`/api/auth/register`)
- Login (`/api/auth/login`)
- Current user (`/api/auth/me`)
- One microservice through gateway (`/api/pets/stats`)
