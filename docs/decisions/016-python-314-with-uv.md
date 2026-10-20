# ADR-016: Python 3.14 managed with uv

- Status: Decided
- Date: 2026-10-19

## Context

F1-T00b asks for a pinned Python version, a virtual environment and a dependency file with pinned versions. On 2026-10-19, Python 3.15 had been out for ten days, 3.14 was in bugfix support until 2030, and 3.13 and older only received security fixes. The ML stack depends on compiled libraries that support a new Python release months after it ships: SHAP depends on Numba, which added Python 3.14 support in its 0.63 release. The same version must be used on the laptop, in CI and in the Docker images.

## Decision

- Python 3.14, pinned in `.python-version`.
- uv manages the Python install, the virtual environment and the dependencies. `pyproject.toml` declares them and `uv.lock` pins every version; both are committed.
- Dependencies are added only with `uv add` (or `uv add --dev`), never with a loose `pip install` or by editing the lockfile.
- `make setup`, CI and Docker install with `uv sync --locked`, which fails if the lockfile does not match `pyproject.toml`.
- `.venv` is never committed.
- uv itself (0.13.3) is installed from its release tarball after a SHA-256 check, not from the `curl | sh` installer. On WSL with the repository on the Windows disk, `UV_LINK_MODE=copy` is set.

## Alternatives discarded

- Python 3.15: too new for the compiled ML libraries (Numba and SHAP).
- Python 3.13: valid, but already in security-only support.
- pip with venv and pip-tools: works, but three tools and Python installed separately.
- Poetry: valid, slower and less common in recent job postings than uv.

## Consequences

The CI (F1-T00f) installs the same uv version and runs `uv sync --locked`; the ingestion image (F1-T11) uses a `python:3.14-slim` base. Upgrading Python is a deliberate change to `.python-version`, `pyproject.toml`, CI and the images at once.
