# ADR-017: Plain SQL migrations with dbmate

- Status: Decided
- Date: 2026-10-20

## Context

F1-T03 writes the first migration and requires it to apply to an empty database and roll back cleanly. The options were Alembic (SQLAlchemy's migration tool) or plain SQL files applied by a small runner. The project has no ORM: the read API only reads and the ingestion job does simple upserts. `06-code-style-guide.md` already proposed plain SQL migrations. Migrations must run as the administrator role, so that the default privileges from `deploy/compose/initdb/10-roles.sh` apply to every new table. Later they run in Kubernetes before the API starts, and they will need `create extension vector` for pgvector (Branch C). Phase F1 is in strict mentor mode: the owner writes the code to learn it.

## Decision

- Migrations are plain SQL files in `db/migrations/`, one file per change, each with a `-- migrate:up` and a `-- migrate:down` section.
- dbmate applies them (`up`, `down`, `status`) and records what ran in its own table.
- After each migration dbmate writes `db/schema.sql`, a full snapshot of the schema that is committed and reviewed with the migration.
- Migrations connect with the administrator `DATABASE_URL`, never with `atalaya_ingest` or `atalaya_api`.
- dbmate is installed as a pinned release binary after a SHA-256 check; in the cluster it runs from its official image pinned by digest (ADR-012).
- A migration that has been merged to `main` is never edited; a fix is a new migration.

## Alternatives discarded

- Alembic: its main strength is autogenerating migrations from SQLAlchemy models, and the project uses no ORM. Without it, migrations become SQL inside Python files, and running them in the cluster needs an image with Python and the project code. It stays a natural choice if an ORM is adopted later.
- golang-migrate: similar, but separate up and down files and no schema snapshot.
- Flyway: standard in Java projects, heavier than needed here.

## Consequences

The owner writes all schema SQL by hand: tables, keys, constraints and indexes. Generating `db/schema.sql` needs a `pg_dump` at least as new as the server (PostgreSQL 18). A Kubernetes Job (F3) runs `dbmate up` before the API deployment.
