.PHONY: setup hooks format db-up db-down db-logs db-reset migrate-new migrate-up migrate-down migrate-status up test lint check scan

COMPOSE := docker compose -f deploy/compose/compose.yaml --env-file .env

setup:
	uv sync --locked
	uv run python --version

# Enables the versioned Git hooks in .githooks/ for this clone.
hooks:
	git config core.hooksPath .githooks

format:
	uv run ruff format .
	uv run ruff check --fix .

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
	uv run pytest

lint:
	uv run ruff format --check .
	uv run ruff check .

scan:
		gitleaks git --redact --verbose 

check: lint test scan
	@echo "check finished: lint, tests and secret scan passed"
