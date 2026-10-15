---
titulo: Tasks Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [00-spec.md, 01-prd.md, 08-testing-guide.md, 09-implementation-plan.md]
---

# Tasks Guide

## How to use this file

- Each task is small enough to finish in one work session.
- Each task has a "Done when" that can be verified.
- Mentor mode: **strict** means the owner writes the code and the AI asks, explains and reviews. **Mixed** means the owner writes the core logic and the AI may generate repetitive parts after the owner explains them. **Flexible** means the AI may generate and the owner must be able to explain the result.
- Update the checkbox and `11-memory.md` at the end of every session.
- Phases F0 to F2 are detailed. Later phases are outlined and refined when the phase starts.

## Phase F0: Repository and documentation (flexible)

- [x] F0-T01 · Create the repository with name and license
  - Done when: repository exists, license file present, name recorded in `11-memory.md`
  - Depends on: none (name decided: Atalaya, repository Atalaya-Coral)
  - Requirement: RF-14
- [x] F0-T02 · Add `docs/` and `AGENTS.md` from this suite
  - Done when: all documents are in the repository and linked from the README
  - Depends on: F0-T01
  - Requirement: governance
- [x] F0-T03 · Write the README skeleton
  - Done when: it has summary, architecture diagram, how to run (marked TODO), and links to `docs/`
  - Depends on: F0-T02
  - Requirement: RF-14
- [ ] F0-T04 · Create the Makefile with `up`, `test`, `lint` and `check` stubs
  - Done when: each target runs and prints what it will do
  - Depends on: F0-T01
  - Requirement: RF-14
- [ ] F0-T05 · Add minimal CI (lint and secret scan)
  - Done when: a pull request runs the pipeline and passes
  - Depends on: F0-T04
  - Requirement: NFR-8, NFR-12
- [ ] F0-T06 · Enable branch protection and a pre-commit hook for secret scanning
  - Done when: a direct push to main is rejected and a fake secret is blocked locally
  - Depends on: F0-T05
  - Requirement: NFR-8
- [x] F0-T07 · Write ADR-001 to ADR-005
  - Done when: five short ADRs exist in `docs/decisions/`
  - Depends on: F0-T02
  - Requirement: governance

**Gate F0:** repository is public-ready, CI is green, documents are in place.

## Phase F1: Ingestion and database (strict)

- [ ] F1-T01 · Decide the first sites
  - Done when: a short list of sites with coordinates is recorded and the 5 km pixel question is checked
  - Depends on: none
  - Requirement: RF-4
- [ ] F1-T02 · Explore the ERDDAP dataset by hand
  - Done when: exact variable names, units and valid ranges are written in `03-architecture.md` (replacing the TO VERIFY marks)
  - Depends on: F1-T01
  - Requirement: RF-1
- [ ] F1-T03 · Write the first migration (`sites`, `observations`, `ingestion_runs`)
  - Done when: the migration applies to an empty database and rolls back cleanly
  - Depends on: F1-T02
  - Requirement: RF-1, RF-2
- [ ] F1-T04 · Download one day for one site and print it
  - Done when: a script prints the values and they match what the web interface shows
  - Depends on: F1-T02
  - Requirement: RF-1
- [ ] F1-T05 · Validate values (ranges and dates)
  - Done when: unit tests cover valid, out-of-range and missing values (TC-3)
  - Depends on: F1-T04
  - Requirement: NFR-4
- [ ] F1-T06 · Write idempotent upserts
  - Done when: running twice leaves identical row counts (TC-1)
  - Depends on: F1-T03, F1-T05
  - Requirement: RF-2
- [ ] F1-T07 · Record every run in `ingestion_runs`
  - Done when: a successful and a failed run both leave a record
  - Depends on: F1-T06
  - Requirement: RF-2
- [ ] F1-T08 · Add retries with backoff
  - Done when: a simulated network failure is retried and recorded (TC-2)
  - Depends on: F1-T07
  - Requirement: NFR-3
- [ ] F1-T09 · Handle missing days
  - Done when: a day without data creates a flagged gap (TC-4)
  - Depends on: F1-T07
  - Requirement: RF-1, NFR-5
- [ ] F1-T10 · Build a resumable backfill command
  - Done when: an interrupted backfill resumes without duplicates and prints a coverage report (TC-5)
  - Depends on: F1-T08
  - Requirement: RF-3
- [ ] F1-T11 · Package ingestion as a container
  - Done when: the container runs the job against the local database
  - Depends on: F1-T10
  - Requirement: RF-14

**Gate F1:** a clean run fills the database for the chosen sites and the ingestion tests pass.

## Phase F2: API and dashboard (mixed)

- [ ] F2-T01 · Create the API skeleton with `/health` and the OpenAPI page
  - Done when: it runs in a container and `/docs` loads
  - Depends on: F1-T11
  - Requirement: RF-5
- [ ] F2-T02 · Implement `GET /sites` and `GET /sites/{id}`
  - Done when: contract tests pass (TC-7, TC-8)
  - Depends on: F2-T01
  - Requirement: RF-5
- [ ] F2-T03 · Implement observations by date range
  - Done when: filters, ordering and cursor pagination work and are tested
  - Depends on: F2-T02
  - Requirement: RF-5
- [ ] F2-T04 · Standard error format and request ID
  - Done when: every error follows `04-api-guide.md`
  - Depends on: F2-T02
  - Requirement: RF-5
- [ ] F2-T05 · Admin endpoints with API key
  - Done when: missing key returns 401 (TC-9) and a site can be added
  - Depends on: F2-T04
  - Requirement: RF-4
- [ ] F2-T06 · Dashboard skeleton with design tokens
  - Done when: tokens from `07-design-guide.md` are in place in both themes
  - Depends on: F2-T02
  - Requirement: RF-6
- [ ] F2-T07 · Site list with `AlertBadge` and all states
  - Done when: loading, empty and error views exist (TC-10)
  - Depends on: F2-T06
  - Requirement: RF-6
- [ ] F2-T08 · Site detail with the time series
  - Done when: a series and a text summary render for a site
  - Depends on: F2-T03, F2-T07
  - Requirement: RF-6
- [ ] F2-T09 · Docker Compose for the core and `make up`
  - Done when: one command starts everything on a clean clone (TC-18)
  - Depends on: F2-T08
  - Requirement: RF-14
- [ ] F2-T10 · Follow the README on a clean machine
  - Done when: the README works literally and any fixes are committed
  - Depends on: F2-T09
  - Requirement: NFR-1

**Gate F2:** release v0.1. The core starts with a single command.

## Phase F3: Kubernetes and GitOps (flexible, owner explains each piece)

Outline, refine at phase start: Dockerfiles for each service; create local cluster; manifests under `deploy/k8s`; install ArgoCD; sync from Git; choose Helm or Kustomize and record an ADR.

**Gate F3:** a change in Git reaches the cluster without manual steps.

## Phase F4: Observability (mixed)

Outline, refine at phase start: expose metrics from ingestion and API; deploy Prometheus, Grafana and Loki; add OpenTelemetry traces; dashboards and alert rules as code; provoke a failure and confirm the alert.

**Gate F4:** a provoked failure raises an alert visible on the dashboards.

## Phase F5: Forecast, Branch A (strict)

Outline, refine at phase start: build features; baseline; temporal split and leakage test; XGBoost; SHAP; write forecasts; expose through the API; compare against the baseline.

Requirements: RF-7, RF-8, RF-9.

**Gate F5:** release v0.2. Forecast beats the baseline and the leakage test passes.

## Phase F6: MLOps, Branch B (mixed)

Outline, refine at phase start: MLflow; scheduled retraining; drift check; notifications through the chosen channel.

Requirements: RF-10, RF-11.

**Gate F6:** release v0.3. A retrain runs on schedule and its result is recorded.

## Phase F7: Agents, Branch C (mixed; agent logic strict)

Outline, refine at phase start: HolmesGPT with read-only access; domain agent with a data context; evaluation set; guardrails; refusal behavior.

Requirements: RF-12, RF-13.

**Gate F7:** release v0.4. Evaluations pass and read-only access is verified.

## Phase F8: Cloud (flexible in configuration, strict in understanding cost)

Outline, refine at phase start: Terraform modules; deploy through GitOps; budget alert; teardown; record cost.

**Gate F8:** release v1.0. Created and destroyed with Terraform within budget.

## Open questions

- [x] Repository name for F0-T01: Atalaya-Coral (decided 2026-10-14).
- [ ] Choice of first sites for F1-T01.

## Related documents

[00-spec.md](00-spec.md) · [01-prd.md](01-prd.md) · [08-testing-guide.md](08-testing-guide.md) · [09-implementation-plan.md](09-implementation-plan.md) · [11-memory.md](11-memory.md)
