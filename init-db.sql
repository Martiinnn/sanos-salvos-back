-- ============================================================
-- Sanos y Salvos — Database Initialization
-- ============================================================

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create schemas for service isolation (Database per Service pattern)
CREATE SCHEMA IF NOT EXISTS pets_service;
CREATE SCHEMA IF NOT EXISTS geo_service;
CREATE SCHEMA IF NOT EXISTS auth_service;

-- ============================================================
-- AUTH SERVICE TABLES
-- ============================================================
CREATE TABLE auth_service.users (
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

-- ============================================================
-- PETS SERVICE TABLES
-- ============================================================
CREATE TABLE pets_service.pets (
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

CREATE TABLE pets_service.reports (
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

CREATE INDEX idx_reports_type ON pets_service.reports(report_type);
CREATE INDEX idx_reports_status ON pets_service.reports(status);
CREATE INDEX idx_reports_pet ON pets_service.reports(pet_id);

-- ============================================================
-- GEOLOCATION SERVICE TABLES
-- ============================================================
CREATE TABLE geo_service.locations (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL,
    coordinates GEOMETRY(POINT, 4326) NOT NULL,
    address TEXT,
    zone VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_coords ON geo_service.locations USING GIST(coordinates);
CREATE INDEX idx_locations_report ON geo_service.locations(report_id);

-- ============================================================
-- SEED DATA (for demo purposes)
-- ============================================================
INSERT INTO auth_service.users (email, username, hashed_password, full_name, phone) VALUES
('demo@sanosysalvos.cl', 'demo', '$2b$12$LJ3m4ys5qOzXHEOMgS/VZeRTk.yD1FMCmXEKi6hGXn2UZJdK0WlEy', 'Usuario Demo', '+56912345678');

-- ============================================================
-- MATCH SERVICE TABLES
-- ============================================================
CREATE SCHEMA IF NOT EXISTS match_service;

CREATE TABLE match_service.matches (
    id UUID PRIMARY KEY,
    report_lost_id INTEGER NOT NULL,
    report_found_id INTEGER NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    score_breakdown JSONB,
    status VARCHAR(20) DEFAULT 'pendiente' CHECK (status IN ('pendiente', 'confirmado', 'descartado')),
    pet_lost_name VARCHAR(100),
    pet_found_name VARCHAR(100),
    user_lost_id INTEGER,
    user_found_id INTEGER,
    notified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_matches_reports ON match_service.matches(report_lost_id, report_found_id);

CREATE TABLE match_service.report_cache (
    report_id INTEGER PRIMARY KEY,
    report_type VARCHAR(20) NOT NULL,
    pet_name VARCHAR(100),
    species VARCHAR(50),
    breed VARCHAR(100),
    color VARCHAR(100),
    size VARCHAR(20),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    date_event DATE,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cache_type ON match_service.report_cache(report_type);

