# ADR-020: How candidate sites are defined

- Status: Decided
- Date: 2026-11-09

## Context

Atalaya needs a list of reef sites in Costa Rica, each tied to the NOAA Coral Reef Watch 0.05 degree cells that describe its water. There are no official coordinates for most reefs, a hand-picked point can fall on land or on a cell that NOAA marks as land, and a reef can be smaller than a cell or span several. F1-T01 (2026-10-23) chose to build the list from mapped coral instead of picking points by hand.

## Decision

Sites are built from data, in four steps, and the result is reproducible with `make sites`.

1. **Areas.** Each candidate area is drawn on the Allen Coral Atlas and its benthic map is downloaded (`data/raw/allen/`, see `data/README.md`). An area is kept only if it has a benthic map and at least 0.1 km² of Coral/Algae. Areas whose coral touches the same NOAA cell are merged into one site.
2. **Search box.** `data/sites/areas.csv` holds one row per site: slug, name, coast, downloads, a box taken from the drawn boundary and rounded outward to 4 decimals, an `active` flag and a quality `note`. This file is curated by the owner.
3. **Point and cells.** The Coral/Algae polygons of the site's downloads are joined and clipped to its box. The site point is the representative point of that coral (always inside it), rounded to 4 decimals. The candidate cells are the 0.05 degree cells whose area overlaps the coral.
4. **Water cells.** The NOAA mask (`CRW_DHW_mask` of dataset `dhw_5km`, fixed date 2026-01-01, value 0 = water) is read from ERDDAP, with the server taken from `ERDDAP_BASE_URL`. A site keeps the water cells under its coral (`cells_from = coral`). If none is water, it takes the water cells around them (`neighbors`), or none (`none`), and the owner reviews it.

`data/sites/sites.csv` is generated and never edited by hand. The ingestion reads only active sites and their cells.

## Result on 2026-11-09

13 sites: 12 active and 1 inactive. Golfo Dulce, Los Mogos is inactive because both cells under its coral are land in the mask and its neighbor cells overlap Ánimas y Dos Ríos. Five areas were discarded before this step (see `data/README.md`).

## Alternatives discarded

- Coordinates picked by hand: not reproducible, and they can land on a cell NOAA marks as land.
- Only the cell of the site point: ignores reefs that span several cells.
- The centroid of the coral: it can fall outside the coral (for example, a horseshoe-shaped reef).
- The latest date of the mask: missing values can change from day to day, so the file would not be reproducible.
- Deleting Los Mogos: it may become usable with a finer temperature product, so it stays as inactive with a note.

## Consequences

- The ingestion (F1-T04 onward) reads `sites.csv`, filters `active = true` and requests the listed cells.
- Bahía Santa Elena has 9 water cells, much wider than the others; split it in `areas.csv` if the model needs it.
- MUR SST (about 1 km, noted on 2026-10-23) is the candidate to revisit Los Mogos and other coastal cells in F5.
- The 2026-11-09 run used the PacIOOS server because NOAA's (upwell) did not answer; both serve the same dataset and mask.
