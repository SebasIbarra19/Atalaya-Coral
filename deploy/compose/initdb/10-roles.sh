#!/bin/sh
# Creates the application roles on the first start of an empty database volume.
# The official PostgreSQL image runs files in /docker-entrypoint-initdb.d only when
# the data directory is empty. Passwords come from .env, never from this file.
#
# Roles (05-security-guide.md, section 3):
#   POSTGRES_USER   administrator; owns the schema and runs migrations
#   atalaya_ingest  ingestion job: read and write rows in schema atalaya
#   atalaya_api     read API: read-only
set -eu

psql -v ON_ERROR_STOP=1 \
     --username "$POSTGRES_USER" \
     --dbname "$POSTGRES_DB" \
     -v db="$POSTGRES_DB" \
     -v admin="$POSTGRES_USER" \
     -v ingest_pw="$ATALAYA_INGEST_PASSWORD" \
     -v api_pw="$ATALAYA_API_PASSWORD" <<'SQL'
-- Nobody connects or creates objects unless granted.
REVOKE ALL ON DATABASE :"db" FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Application schema, owned by the administrator.
CREATE SCHEMA atalaya AUTHORIZATION :"admin";

CREATE ROLE atalaya_ingest LOGIN PASSWORD :'ingest_pw';
CREATE ROLE atalaya_api    LOGIN PASSWORD :'api_pw';

GRANT CONNECT ON DATABASE :"db" TO atalaya_ingest, atalaya_api;
GRANT USAGE ON SCHEMA atalaya TO atalaya_ingest, atalaya_api;

-- Tables created later by the administrator (migrations) get these grants automatically.
ALTER DEFAULT PRIVILEGES FOR ROLE :"admin" IN SCHEMA atalaya
  GRANT SELECT, INSERT, UPDATE ON TABLES TO atalaya_ingest;
ALTER DEFAULT PRIVILEGES FOR ROLE :"admin" IN SCHEMA atalaya
  GRANT USAGE, SELECT ON SEQUENCES TO atalaya_ingest;
ALTER DEFAULT PRIVILEGES FOR ROLE :"admin" IN SCHEMA atalaya
  GRANT SELECT ON TABLES TO atalaya_api;

-- Unqualified table names resolve to schema atalaya.
ALTER ROLE atalaya_ingest SET search_path = atalaya;
ALTER ROLE atalaya_api    SET search_path = atalaya;
ALTER ROLE :"admin"       SET search_path = atalaya, public;
SQL
