# ADR-002: XGBoost with SHAP, starting from a baseline

- Status: Decided
- Date: 2026-10-10
- Corrected: 2026-11-06 (the context said the reference study was for Costa Rica; it covered Florida)

## Context

The forecast must be explainable and comparable. Arcodia et al. (2025) used this approach on three Florida reef sites with data from 1985 to 2024: XGBoost forecast the onset of moderate heat stress up to six weeks ahead, and SHAP showed which factors drove each forecast (Environmental Research Communications, December 2025). Atalaya applies the same approach to Costa Rican sites.

## Decision

Build a trivial baseline first (persistence), then XGBoost with SHAP explanations. XGBoost must beat the baseline on a held-out period.

## Alternatives discarded

- Neural networks: more complex and less explainable at this data size.

## Consequences

Temporal splits and a leakage test are required (F5). Success is measured against the baseline, not an absolute score.
