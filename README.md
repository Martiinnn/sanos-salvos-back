# 🐾 Sanos y Salvos

Plataforma fullstack de microservicios para la localización y recuperación de mascotas perdidas.

## Arquitectura

| Componente | Tecnología | Puerto |
|---|---|---|
| **Frontend** | React 18 + Vite | 5173 |
| **API Gateway** | FastAPI + JWT + Circuit Breaker | 8000 |
| **Gestión de Mascotas** | FastAPI + PostgreSQL | 8001 |
| **Geolocalización** | FastAPI + PostGIS | 8002 |
| **Motor de Match** | FastAPI + MongoDB | 8003 |
| **Notificaciones** | FastAPI + WebSocket | 8004 |
| **Message Broker** | RabbitMQ | 5672 / 15672 |
| **Base de Datos** | PostgreSQL 16 + PostGIS | 5432 |
| **Base NoSQL** | MongoDB 7 | 27017 |

## Patrones Implementados

- **API Gateway** — Punto de entrada centralizado con JWT
- **Database per Service** — Cada servicio con su propia base de datos
- **Repository Pattern** — Abstracción de acceso a datos
- **Factory Method** — Creación de reportes y matches especializados
- **Circuit Breaker** — Resiliencia ante fallos de servicios
- **Event-Driven Architecture** — Comunicación asíncrona con RabbitMQ

## Requisitos

- Docker y Docker Compose

## Instalación y Ejecución

```bash
# Clonar repositorio
git clone <repo-url>
cd proyecto-fullstack

# Levantar todo el stack
docker-compose up --build

# Acceder a la aplicación
# Frontend:     http://localhost:5173
# API Gateway:  http://localhost:8000/docs
# RabbitMQ:     http://localhost:15672 (guest/guest)
```

## Credenciales Demo

- **Email:** demo@sanosysalvos.cl
- **Password:** demo123

## Equipo

- Martín Leiva Andrades
- Matías Flores Pastene

**Asignatura:** Desarrollo Full Stack III 001D  
**Docente:** Eduardo Antonio Valenzuela Acevedo
