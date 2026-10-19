# ADR-008: Phoenix for LLM observability

- Status: Proposed
- Date: 2026-10-18

## Context

Every model call should be traceable: prompt, answer, tokens, latency and tool calls (TR-14). The local machine has 16 GB of RAM shared with the cluster and the observability stack.

## Decision

Use Arize Phoenix, open source, as a single container. It receives OpenTelemetry traces, which the project already uses (F4).

## Alternatives discarded

- Langfuse self-hosted: good tool, but its current self-hosted setup needs several extra services (PostgreSQL, ClickHouse, Redis and object storage), too heavy for the laptop next to the rest of the stack.
- Hosted services: outside the zero-cost rule.

## Consequences

LLM traces live in Phoenix and system metrics in Grafana. If Phoenix falls short, Langfuse can be evaluated later; both accept OpenTelemetry.
