# ADR-005: PostgreSQL for observations

- Status: Proposed
- Date: 2026-10-14

## Context

Data is daily values for a small number of sites: low volume, relational (sites, observations, forecasts, runs).

## Decision

Store everything in plain PostgreSQL, with upserts keyed by site and date.

## Alternatives discarded

- A specialized time-series database: not needed at this volume; evaluated only if volume demands it.

## Consequences

One database to operate. Open question: whether a time-series extension is needed (see `03-architecture.md`).
