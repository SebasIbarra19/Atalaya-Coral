.PHONY: setup db-up db-down db-logs db-reset migrate-new migrate-up migrate-down migrate-status up test lint check scan

COMPOSE := docker compose -f deploy/compose/compose.yaml --env-file .env

setup:
	uv sync --locked
	uv run python --version

db-up:
	$(COMPOSE) --profile core up -d db
	$(COMPOSE) --profile core ps

db-down:
	$(COMPOSE) --profile core down

db-logs:
	$(COMPOSE) --profile core logs -f db

# Deletes the local database volume and recreates it, so the init scripts run again.
db-reset:
	@echo "This deletes ALL local database data. Press Ctrl+C within 5 seconds to cancel."
	@sleep 5
	$(COMPOSE) --profile core down -v
	$(COMPOSE) --profile core up -d db
	$(COMPOSE) --profile core ps

# Migrations (ADR-017). dbmate reads DATABASE_URL (administrator) from .env.
migrate-new:
	@test -n "$(name)" || (echo "usage: make migrate-new name=create_sites" && exit 1)
	dbmate new $(name)

migrate-up:
	dbmate up

migrate-down:
	dbmate down

migrate-status:
	dbmate status

up:
	@echo "[stub] will start the local core stack (database, ingestion, API, dashboard). Defined in F2-T09."

test:
	@echo "[stub] will run the test suites. Defined when the first tests exist (F1)."

lint:
	@echo "[stub] will run formatters and linters. Defined in F1."

scan:
		gitleaks git --redact --verbose 

check: lint test scan
	@echo "[stub] check finished (all targets are still stubs)."
