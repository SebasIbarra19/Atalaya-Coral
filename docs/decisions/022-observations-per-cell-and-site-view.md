# ADR-022: Observations stored per cell, sites read through a view

- Status: Decided
- Date: 2026-11-12
- Builds on: ADR-020 (how sites and their cells are defined), ADR-021 (alert level)

## Context

ADR-020 gives each site between 2 and 9 NOAA cells of 0.05 degrees, and one cell is shared by two sites (Golfo Dulce). Each cell has its own daily values, but the data model in `03-architecture.md` had one row per site and day, without saying how several cells become one value. F1-T03 writes the first migration, so the choice has to be made now.

NOAA faces the same question in its 5 km Regional Virtual Stations: it takes the 90th percentile HotSpot among the station's pixels and reads the other variables from the pixel where that value occurs, so the chosen pixel moves as the heat stress moves (https://coralreefwatch.noaa.gov/product/vs/map.php).

## Decision

1. **Raw data per cell.** `cell_observations` stores one row per cell and day, as NOAA publishes it, keyed by (`cell_id`, `date`). `cells` holds each cell center once, and `site_cells` links sites to cells, so a shared cell is downloaded and stored once.
2. **Site values through a view.** `site_observations` gives one row per site and day, taken whole from the site's most stressed cell that day: highest `alert_level`, then highest `dhw`, then highest `hotspot` (ties broken by `cell_id`). All values of a row come from one real cell, so the alert level always matches its own HotSpot and DHW.
3. With 2 to 9 cells per site, the most stressed cell is close to NOAA's 90th percentile, and it leans toward alerting rather than hiding the warmest corner of a reef.

## Alternatives discarded

- Storing values already combined per site: loses the raw data, and any change of rule means downloading the whole history again.
- Averaging the cells: can hide the part of the reef that is under stress.
- Mixing the maximum of each variable from different cells: gives combinations that no cell had (for example, an alert level that does not match the DHW shown).
- Recomputing DHW from the site's HotSpot series, as NOAA does for its stations: closer to NOAA, but more code before there is a model to need it. Revisit in F5.

## Consequences

- The ingestion requests cells, not sites, and writes `cell_observations`.
- The API and the model read `site_observations`; the view is covered by the default `SELECT` grant of `atalaya_api`.
- The full history for the 12 active sites is about 44 cells times 15 188 days, about 670 000 rows: small for PostgreSQL.
- A new task loads `data/sites/sites.csv` into `sites`, `cells` and `site_cells`.
