import os
import psycopg2


def env(name: str, default: str) -> str:
    return os.getenv(name, default)


SQL = """
CREATE SCHEMA IF NOT EXISTS auth_service;
CREATE SCHEMA IF NOT EXISTS pets_service;

CREATE TABLE IF NOT EXISTS auth_service.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pets_service.pets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    species VARCHAR(50) NOT NULL DEFAULT 'perro',
    breed VARCHAR(100),
    color VARCHAR(100) NOT NULL,
    size VARCHAR(20) NOT NULL CHECK (size IN ('pequeño', 'mediano', 'grande')),
    age_estimate VARCHAR(50),
    description TEXT,
    photo_url TEXT,
    distinctive_features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pets_service.reports (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER NOT NULL REFERENCES pets_service.pets(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    report_type VARCHAR(20) NOT NULL CHECK (report_type IN ('perdido', 'encontrado')),
    status VARCHAR(20) NOT NULL DEFAULT 'activo' CHECK (status IN ('activo', 'resuelto', 'expirado')),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    address TEXT,
    date_event DATE,
    contact_name VARCHAR(200),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reports_type ON pets_service.reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_status ON pets_service.reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_pet ON pets_service.reports(pet_id);
"""


def main() -> None:
    conn = psycopg2.connect(
        host=env("POSTGRES_HOST", "localhost"),
        port=env("POSTGRES_PORT", "5432"),
        dbname=env("POSTGRES_DB", "sanosysalvos_db"),
        user=env("POSTGRES_USER", "sanosysalvos"),
        password=env("POSTGRES_PASSWORD", "sanosysalvos2026"),
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(SQL)
    conn.close()
    print("Local DB initialized for auth + pets services.")


if __name__ == "__main__":
    main()
