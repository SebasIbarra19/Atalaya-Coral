# ADR-002: XGBoost with SHAP, starting from a baseline

- Status: Decided
- Date: 2026-10-10

## Context

The forecast must be explainable and comparable. Arcodia et al. (2025) used a similar approach for Costa Rica with good results.

## Decision

Build a trivial baseline first (persistence), then XGBoost with SHAP explanations. XGBoost must beat the baseline on a held-out period.

## Alternatives discarded

- Neural networks: more complex and less explainable at this data size.

## Consequences

Temporal splits and a leakage test are required (F5). Success is measured against the baseline, not an absolute score.
