# Arquitectura de repositorio — Incremento 02 (base)

- **Frontend**: React / TypeScript con Vite; aplicación SPA responsiva.
- **API**: FastAPI y SQLModel; seguridad con token JWT de duración limitada.
- **Persistencia**: PostgreSQL en Docker; SQLite opcional para desarrollo local.
- **Migraciones**: Alembic. La revisión 0001 crea tablas del núcleo con metadatos ORM.
- **Dominios implementados**: usuarios, membresías, instituciones, programas y competencias.
- **API implementada**: `POST /v1/auth/login`, `GET /v1/me`, `GET /v1/institutions`, `GET/POST /v1/programs`, `GET/POST /v1/competencies`, `GET /health`.
- **Diferencias respecto a los planos**: no existen todavía endpoints de planificación, evaluación, entregas o seguimiento. Tampoco hay alta pública de instituciones, ni registro público de usuarios. Los códigos institucionales deben validarse antes de registrar datos reales.
- **Límites**: seguridad básica de desarrollo, no apta para producción (faltan protección de abuso, rotación/revocación, revisión de sesión, invitaciones, RGPD/legislación aplicable, copias de seguridad, pruebas integrales y controles de acceso adicionales).
- **No confundir**: `create_all` en la migración inicial simplifica el arranque; futuras revisiones deben usar operaciones Alembic explícitas y comprobadas.
