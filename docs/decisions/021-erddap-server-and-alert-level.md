# ADR-021: ERDDAP server and computed alert level

- Status: Decided
- Date: 2026-11-12
- Updates: the 2026-10-23 decision in `11-memory.md` (NOAA primary, PacIOOS fallback)

## Context

F1-T02 explored the dataset `dhw_5km` (NOAA Coral Reef Watch, daily global 5 km) by hand on 2026-11-12. Two findings change earlier assumptions.

1. **Server.** NOAA's own ERDDAP servers (`upwell.pfeg.noaa.gov` and `coastwatch.pfeg.noaa.gov`) timed out after 20 seconds on 2026-10-23, 2026-11-09 and 2026-11-12. The PacIOOS mirror (`pae-paha.pacioos.hawaii.edu/erddap`) answered in under a second, and its latest day was 2026-11-11, one day behind. The earlier note that the mirror "can lag weeks" was an assumption, not a measurement.
2. **Alert level.** In this dataset `CRW_BAA` has five values, 0 to 4 (`no_stress watch warning alert_level1 alert_level2`). NOAA added Alert Levels 3 to 5 on 2023-12-15, and Atalaya already uses the eight-level scale (`07-design-guide.md`). The data shows the gap: on 2026-11-07, Bahía Culebra (cell -85.675, 10.625) had HotSpot 1.03 and DHW 12.07, which is Alert Level 3 on NOAA's current scale, but `CRW_BAA` was 4 (Alert Level 2).

## Decision

**Server.** PacIOOS is the default ERDDAP server in `.env.example`. NOAA's server stays documented as an alternative. The URL is configuration (`ERDDAP_BASE_URL`), and every run records which server it used in `ingestion_runs`.

**Alert level.** Atalaya computes the alert level from HotSpot and DHW with NOAA's current table, in a pure function:

| Code | Level | Rule |
| --- | --- | --- |
| 0 | No stress | HotSpot <= 0 |
| 1 | Bleaching Watch | 0 < HotSpot < 1 |
| 2 | Bleaching Warning | HotSpot >= 1 and 0 < DHW < 4 |
| 3 | Alert Level 1 | HotSpot >= 1 and 4 <= DHW < 8 |
| 4 | Alert Level 2 | HotSpot >= 1 and 8 <= DHW < 12 |
| 5 | Alert Level 3 | HotSpot >= 1 and 12 <= DHW < 16 |
| 6 | Alert Level 4 | HotSpot >= 1 and 16 <= DHW < 20 |
| 7 | Alert Level 5 | HotSpot >= 1 and DHW >= 20 |

`CRW_BAA` is stored too, as NOAA's own value. Codes 0 to 4 mean the same in both, so the computed level capped at 4 must equal `CRW_BAA`: unit tests cover every threshold, and the ingestion logs any day where the two disagree (small differences at exact thresholds can come from values rounded to 2 decimals).

Source of the table: NOAA Coral Reef Watch, Satellite Bleaching Alert stress levels (updated 2023-12-15), https://coralreefwatch.noaa.gov/subscriptions/vs.php

## Alternatives discarded

- NOAA as default: it did not answer on three different days; nearly every run would need the fallback.
- Using `CRW_BAA` as the alert level: it stops at Alert Level 2, so any reef above 12 DHW (Bahía Culebra in November 2026) would be shown with less stress than NOAA itself reports.
- Computing the level without storing `CRW_BAA`: no way to check the function against NOAA.

## Consequences

- F1-T03: `observations` gets `crw_baa` (0 to 4) and `alert_level` (0 to 7); `ingestion_runs` gets the server URL.
- F1-T05: the alert function and its tests are part of value validation.
- When NOAA's servers answer again, check whether their copy of `dhw_5km` already has the eight levels; if so, revisit this ADR.
