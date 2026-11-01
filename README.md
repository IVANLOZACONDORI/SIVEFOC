# SIVEFOC — Repositorio inicial (Incremento 02 · base técnica)

Prototipo de desarrollo de **SIVEFOC**: React + TypeScript, FastAPI, PostgreSQL, Alembic y Docker Compose. Incluye login de demostración, instituciones accesibles, programas y competencias con permisos institucionales. **No está validado institucionalmente ni listo para producción.**

## Requisitos

- Docker Desktop con Docker Compose; VS Code y Git (recomendado).
- Para ejecución sin Docker: Python 3.12, Node.js 22, PostgreSQL 16.

## Inicio rápido (VS Code, PowerShell o terminal)

```bash
git init
cp .env.example .env
# Edita .env; cambia POSTGRES_PASSWORD, DATABASE_URL, SECRET_KEY y DEMO_BOOTSTRAP_PASSWORD
# ¡La contraseña en DATABASE_URL debe coincidir con POSTGRES_PASSWORD!
docker compose up --build -d
docker compose exec -e DEMO_BOOTSTRAP_EMAIL=admin@sivefoc.local -e DEMO_BOOTSTRAP_PASSWORD='tu-clave-segura-de-12-o-mas' api python -m scripts.bootstrap
```

En **PowerShell**, sustituye `cp` por `Copy-Item .env.example .env` si fuera necesario. Puedes fijar `DEMO_BOOTSTRAP_PASSWORD` en el `.env` antes de ejecutar el siguiente comando más corto:

```bash
docker compose exec -e DEMO_BOOTSTRAP_EMAIL=admin@sivefoc.local -e DEMO_BOOTSTRAP_PASSWORD='tu-clave-segura-de-12-o-mas' api python -m scripts.bootstrap
```

- Interfaz: http://localhost:5173
- API Swagger: http://localhost:8000/docs
- Salud: http://localhost:8000/health

**Nota:** `docker compose up` no crea el usuario. `bootstrap` debe ejecutarse una vez y falla de forma segura si ya existe. Para acceder, usa el correo y contraseña definidos en bootstrap.

## Desarrollo y pruebas

```bash
# Tests backend desde contenedor
docker compose exec api python -m pytest -q
# Ver logs
docker compose logs -f api
# Migraciones
docker compose exec api alembic current
# Detener sin borrar datos
docker compose down
```

Para desarrollar frontend con recarga rápida local: `cd frontend && npm install && npm run dev`. La SPA del contenedor usa Nginx con el build realizado en `docker compose up --build`.

## Publicar en GitHub (repositorio nuevo y vacío)

```bash
git add .
git commit -m "chore: bootstrap SIVEFOC monorepo"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sivefoc.git
git push -u origin main
```

Primero crea el repositorio vacío en GitHub y autentícate mediante Git Credential Manager o GitHub CLI (`gh auth login`). Nunca publiques `.env`, contraseñas ni datos académicos. Si `git init` no se ejecutó aún, úsalo antes de `git add`.

## Estado y límites

- Implementado en código: autenticación básica JWT; lectura autorizada de instituciones; lectura/escritura acotada de programas y competencias; auditoría de altas; primera migración de datos.
- Pendiente de validación: ejecución de Docker, Postgres, integración backend-frontend, pruebas de aislamiento y reglas de la institución.
- No desarrollado: perfiles de egreso, aula virtual, planificación, rúbricas, evaluación, agente IA, gestión documental y demás módulos.
- No se utilizan datos ni reglamentos militares reales.

Consulta `docs/ARQUITECTURA.md` para decisiones técnicas y límites de seguridad.
