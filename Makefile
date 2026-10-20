.PHONY: setup up test lint check scan

setup:
	uv sync --locked
	uv run python --version

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
