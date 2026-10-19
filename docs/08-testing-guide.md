---
titulo: Testing Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [01-prd.md, 02-trd.md, 06-code-style-guide.md]
---

# Testing Guide

Tools, thresholds and commands are Proposed until the first tests exist. The goal is confidence, not a coverage number.

## 1. Goals

| Goal | Risk it covers |
| --- | --- |
| Ingestion is correct and repeatable | Duplicate or missing data silently corrupts everything downstream |
| The model does not leak the future | A flattering but meaningless forecast |
| The API honors its contract | A change breaks the dashboard or the agent |
| The agent does not invent | Wrong guidance presented as fact |
| The whole system starts from a clean clone | The README stops working without anyone noticing |

## 2. Strategy by level

| Level | What it tests | Tools (Proposed) | When it runs |
| --- | --- | --- | --- |
| Unit | Pure functions: validation, feature building, alert-transition logic | pytest, Vitest | Every commit (local) and CI |
| Integration | Ingestion against a real PostgreSQL; API against the database | pytest with a throwaway database container | CI |
| Contract | API responses match the documented format | Schema-based tests from the OpenAPI file | CI |
| ML checks | Leakage test, baseline comparison, reproducibility with a fixed seed | pytest | CI (small data) and on training |
| Agent evaluations | Answers grounded in data, refusal outside data, schema-valid output, resistance to injection | A versioned evaluation set and a runner script | CI on changes to the agent, prompts or tools (small model or recorded answers `[TO CONFIRM in F7]`); full set before publishing |
| End to end | Dashboard happy path | Playwright | CI on main, nightly later |
| Smoke | Clean clone starts and answers a health check | Shell script in CI | Every pull request |

## 3. Test cases

| ID | Verifies | Level | Priority | Covers |
| --- | --- | --- | --- | --- |
| TC-1 | Running ingestion twice for the same date leaves identical row counts | Integration | High | RF-2, NFR-2 |
| TC-2 | A failed download is retried with backoff and recorded as failed when exhausted | Integration | High | RF-2, NFR-3 |
| TC-3 | Values outside the valid range are rejected and logged | Unit | High | NFR-4 |
| TC-4 | A day with no data creates a flagged gap and raises the missing-data metric | Integration | High | RF-1, NFR-5 |
| TC-5 | Backfill resumes after interruption without duplicates | Integration | Medium | RF-3 |
| TC-6 | Adding a site makes the next ingestion include it | Integration | Medium | RF-4 |
| TC-7 | Each API endpoint returns the documented format | Contract | High | RF-5 |
| TC-8 | Unknown site returns 404 with the standard error body | Contract | High | RF-5 |
| TC-9 | Admin endpoint without a key returns 401 | Contract | High | RF-4, NFR-9 |
| TC-10 | The dashboard shows loading, empty and error states | End to end | Medium | RF-6 |
| TC-11 | No training row is later than the first evaluation row | ML check | High | RF-9 |
| TC-12 | The forecast beats the persistence baseline on the held-out period | ML check | High | RF-7, RF-8, NFR-7 |
| TC-13 | Same seed and data give the same metrics | ML check | Medium | TR-7 |
| TC-14 | A simulated alert-level rise sends exactly one notification | Integration | Medium | RF-11 |
| TC-15 | The agent cites site and date, and refuses a question outside the data | Agent evaluation | High | RF-12 |
| TC-16 | The agent never states a figure that is not in the data it received | Agent evaluation | High | RF-12 |
| TC-17 | HolmesGPT credentials cannot modify cluster state | Security check | High | RF-13, NFR-9 |
| TC-18 | A clean clone starts with the documented command | Smoke | High | RF-14, NFR-1 |
| TC-19 | No secret is present in the repository | Security check | High | NFR-8 |
| TC-20 | A scheduled retrain records parameters, metrics and artifacts, and the drift check reports a result | Integration | Medium | RF-10, TR-9 |
| TC-21 | For a provoked failure, the operations agent returns a probable cause using read-only access | Agent evaluation | Medium | RF-13 |
| TC-22 | Every agent answer validates against the output schema (text, sources, data used) | Agent evaluation | High | RF-12, TR-11 |
| TC-23 | Document search returns the expected reference for a set of known questions | Integration | Medium | RF-12, TR-11 |
| TC-24 | Instructions hidden in a question or in a retrieved document do not change the agent's behavior or tools | Agent evaluation | High | RF-12 |
| TC-25 | A question to the agent produces a trace in Phoenix with tokens and tool calls | Integration | Medium | TR-14 |

Expand this table when a phase begins. Every Must requirement in the PRD needs at least one test case.

## 4. Checklists

**Before each commit**

- [ ] Formatter and linter pass.
- [ ] Unit tests for the changed code pass.
- [ ] No secrets or `.env` files staged.

**Before merging**

- [ ] CI is green (lint, types, tests, build).
- [ ] New behavior has a test; a fixed bug has a regression test.
- [ ] Documents affected by the change are updated.
- [ ] `11-memory.md` and `10-tasks.md` reflect the change.

**Before a release**

- [ ] Smoke test passes on a clean clone.
- [ ] Security checklist in `05-security-guide.md` is complete.
- [ ] Agent evaluations pass.
- [ ] README steps were followed literally by the author on a clean machine.

## 5. Tools and setup

| Need | Tool (Proposed) | Command `[TO CONFIRM when it exists]` |
| --- | --- | --- |
| Python tests | pytest | `make test` |
| Python lint and format | Ruff | `make lint` |
| Type check | mypy or pyright | `make typecheck` |
| Frontend tests | Vitest | `make test-web` |
| End to end | Playwright | `make e2e` |
| Load test | k6 | `make load` |
| Code and image scanning | CodeQL, Trivy | CI only |
| Secret scan | gitleaks | `make scan` |
| Agent evaluations | Runner script | `make eval` |
| Everything | | `make check` |

Setup rules: tests must not need real credentials, tests must not call external services unless marked, and the database used in tests is created and destroyed per run.

## 6. Test data and environments

- Keep a small, versioned sample of NOAA responses for tests so they do not depend on the network.
- Mark any test that needs the live NOAA service and run it separately.
- Generate synthetic sites for tests; do not use real data as fixtures if it is large.
- Evaluation sets for agents are versioned files with question, expected behavior and the data given.

## 7. Quality criteria

| Criterion | Value | Status |
| --- | --- | --- |
| CI must pass to merge | Required | Proposed |
| Minimum coverage | `[TO DEFINE after the first tests exist]` | Open |
| Flaky tests | Fixed or removed, never ignored | Proposed |
| Agent evaluations | Must pass in CI to merge changes to the agent, and before publishing | Proposed |

## Open questions

- [ ] Coverage target, if any.
- [ ] Whether to run end-to-end tests on every pull request.
- [ ] Format of the agent evaluation set.

## Related documents

[01-prd.md](01-prd.md) · [02-trd.md](02-trd.md) · [05-security-guide.md](05-security-guide.md) · [06-code-style-guide.md](06-code-style-guide.md) · [10-tasks.md](10-tasks.md)
