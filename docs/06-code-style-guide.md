---
titulo: Code Style Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [03-architecture.md]
---

# Code Style Guide

Tools and versions here are Proposed until approved. Rules that can be automated are enforced by tools in CI, not by memory.

## 1. General principles

1. **Readability first.** Code is read far more than written. Choose the clear option over the clever one.
2. **Small and focused.** Functions do one thing. Modules have one reason to change.
3. **Consistency over preference.** Follow the existing pattern unless there is a documented reason to change it.
4. **No duplication of knowledge.** If a rule or value lives in two places, one will drift.
5. **Explicit over implicit.** Prefer typed, named and visible behavior over magic.
6. **Leave it tested.** A change that matters comes with a test that would have caught the mistake.

## 2. Technology and code standards

| Area | Standard | Enforced by |
| --- | --- | --- |
| Python version | 3.14, pinned in `.python-version` (ADR-016) | `uv sync --locked` in CI and Docker |
| Python environment and dependencies | uv: `pyproject.toml` plus a committed `uv.lock`; add packages with `uv add`; install with `make setup` (`uv sync --locked`); `.venv` is never committed | CI fails if the lockfile is out of date |
| Python formatting and linting | Ruff (format and lint; rules E, F, I, B, UP; config in `pyproject.toml`). `make lint` checks, `make format` fixes. Ruff also checks Python blocks inside Markdown | Versioned pre-commit hook (`.githooks/`, enabled with `make hooks`), CI |
| Python typing | Type hints on all public functions; mypy or pyright in strict-ish mode `[TO DEFINE]` | CI |
| Python tests | pytest, tests in `tests/`; `make test` | Versioned pre-commit hook, CI |
| TypeScript | `strict` mode on; no `any` without a comment explaining why | tsc, ESLint |
| TypeScript formatting | Prettier | pre-commit, CI |
| SQL | Plain SQL migrations applied with dbmate, one file per change with `-- migrate:up` and `-- migrate:down` (ADR-017); a merged migration is never edited; lowercase keywords or consistent uppercase `[TO DEFINE in F1-T03]` | Review; `dbmate status` in CI |
| Shell | `set -euo pipefail` in scripts; ShellCheck | CI |
| Containers | One process per container, non-root user, pinned base image tags | Review, image scan |
| Commits | Conventional Commits | commit-msg hook or CI check |

## 3. Project structure

See `03-architecture.md`, section 6. Rules:

- Each service lives under `services/<name>/` and has its own README, tests and dependency file.
- Business logic does not live in request handlers or in notebooks. Handlers call functions; notebooks import from the package.
- Dependency direction is one way: handlers, then services, then data access. Data access never imports handlers.
- Configuration is read in one place per service and passed down, not read from the environment all over the code.
- Notebooks are for exploration. Anything that must run repeatedly is moved to a module with tests.

## 4. Error handling

- **Fail loudly at the boundary, recover quietly inside.** Validate inputs where they enter; do not scatter checks everywhere.
- Raise specific exceptions with a clear message. Do not use bare `except` or swallow errors.
- Retry only what is safe to retry (reads, idempotent writes) and always with a limit and backoff.
- Errors crossing the API boundary follow the format in `04-api-guide.md`.
- Log the error once, at the layer that handles it, with a request or run identifier.
- Never log secrets, tokens or full user input.
- Ingestion errors are recorded in `ingestion_runs` and exposed as metrics, so they are visible without reading logs.

## 5. Naming conventions

| Item | Convention | Example |
| --- | --- | --- |
| Python modules, functions, variables | `snake_case` | `load_observations` |
| Python classes | `PascalCase` | `SiteRepository` |
| Python constants | `UPPER_SNAKE_CASE` | `DEFAULT_PAGE_SIZE` |
| TypeScript variables, functions | `camelCase` | `fetchSites` |
| TypeScript types, React components | `PascalCase` | `SiteCard` |
| Files (Python) | `snake_case.py` | `site_repository.py` |
| Files (React components) | `PascalCase.tsx` | `SiteCard.tsx` |
| Database tables | plural `snake_case` | `observations` |
| Database columns | `snake_case` | `alert_level` |
| API paths | plural, lowercase, kebab-case | `/sites/{site_id}/observations` |
| Environment variables | `UPPER_SNAKE_CASE`, prefixed by service when needed | `API_DATABASE_URL` |
| Branches | `type/short-description` | `feat/ingestion-idempotency` |
| Commits | `type(scope): summary` | `feat(ingestion): upsert by site and date` |

Names describe what something is or does. Avoid abbreviations unless they are standard in the domain (for example `sst`, `dhw`).

## 6. Code formatting

- Formatting is automatic. Do not argue about it in review.
- Line length: the formatter's default, unless the team agrees otherwise `[TO DEFINE in F0]`.
- Imports are sorted by the tool.
- One statement per line. No trailing whitespace. Files end with a newline.
- Keep functions short enough to read without scrolling.

## 7. Comments and documentation

- Comment the **why**, not the what. If a comment explains what the code does, rename or restructure instead.
- Every public function, class and module has a docstring or doc comment with purpose, parameters, return value and errors that matter.
- Mark open work with `TODO(owner): ...` and link a task ID from `10-tasks.md`.
- Record non-obvious decisions as short ADRs in `docs/decisions/`, not in code comments.
- Update the relevant document in the same change when behavior changes. The README must always work for a clean clone.

## 8. Short examples

**Naming (Python)**

```python
# Good
def load_observations(site_id: str, start: date, end: date) -> list[Observation]: ...


# Bad
def get(s, a, b): ...
```

**Error handling (Python)**

```python
# Good: specific, with context
try:
    data = client.fetch(site, day)
except NetworkError as exc:
    raise IngestionError(f"fetch failed for {site.id} on {day}") from exc

# Bad: hides the problem
try:
    data = client.fetch(site, day)
except Exception:
    pass
```

**Comment (why, not what)**

```python
# NOAA publishes the latest day with a delay, so we ask for the previous day too.
```

The last example describes a behavior to confirm in F1 `[TO VERIFY]`.

## Open questions

- [x] Python version: 3.14 with uv (ADR-016, 2026-10-19).
- [ ] Type checker.
- [ ] Line length and SQL keyword case.
- [ ] Commit message enforcement.

## Related documents

[03-architecture.md](03-architecture.md) · [04-api-guide.md](04-api-guide.md) · [05-security-guide.md](05-security-guide.md) · [08-testing-guide.md](08-testing-guide.md) · [AGENTS.md](../AGENTS.md)
