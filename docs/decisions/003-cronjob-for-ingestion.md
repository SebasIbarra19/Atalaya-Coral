# ADR-003: Kubernetes CronJob instead of Airflow for ingestion

- Status: Proposed
- Date: 2026-10-14

## Context

Ingestion is one daily task: download NOAA data for a few sites, validate it, upsert it, log the run.

## Decision

Run ingestion as a Kubernetes CronJob (a plain scheduled container locally before F3).

## Alternatives discarded

- Airflow: too heavy for one daily task; adds a scheduler, a database and a web server to operate.

## Consequences

Retries, idempotency and run logging live in the job itself (`ingestion_runs`). Revisit if many dependent tasks appear.
