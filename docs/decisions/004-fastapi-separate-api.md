# ADR-004: FastAPI separate from the dashboard

- Status: Proposed
- Date: 2026-10-14

## Context

The data is read by the dashboard and by agents. The API contract should not depend on the frontend.

## Decision

Serve data through a separate FastAPI service. The Next.js dashboard is only a client of that API.

## Alternatives discarded

- Next.js API routes: would mix data and presentation, and agents would depend on the frontend deployment.

## Consequences

Two services to deploy. FastAPI generates the OpenAPI contract used by contract tests.
