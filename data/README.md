# Data

Raw inputs are not committed (`data/raw/` and `data/processed/` are in `.gitignore`). This file records where each input comes from, how it was obtained and how to cite it, so the folder can be rebuilt on a clean machine.

## Layout

```
data/
  README.md                  this file (committed)
  sites/                     site list built by F1-T01d (committed)
  raw/                       not committed
    allen/
      <area>/<area>-<timestamp>/   one Allen Coral Atlas download, unzipped
      _discarded/                  downloads reviewed and set aside (see below)
      _zips/                       original zip files, as downloaded
```

`<timestamp>` is the one the Atlas puts in the download name (`YYYYMMDDhhmmss`). Scripts read paths from `data/sites/areas.csv`, never from folder names.

## Allen Coral Atlas

**What it is.** Global maps of shallow tropical coral reef habitats, made from Planet Dove satellite imagery with machine learning. Atalaya uses the benthic map to place each site on mapped coral habitat (F1-T01).

**Downloaded on** 2026-10-24 (14 areas) and 2026-11-06 (5 areas), by the owner, from https://allencoralatlas.org.

**How.** For each candidate area: draw the area of interest on the Atlas map, select the benthic map in GeoJSON, download the zip, unzip it into `data/raw/allen/<area>/` and rename the folder to `<area>-<timestamp>`. Keep the zip in `_zips/`.

**Each download contains**

| Path | Content |
| --- | --- |
| `Benthic-Map/benthic.geojson` | Benthic polygons, CRS84 (longitude, latitude), one property `class` |
| `boundary/boundary.geojson` | The area drawn on the Atlas |
| `stats/statistics.csv` | Area per class in km² (benthic, geomorphic and reef extent) |
| `1-License-and-Documentation/` | License, citation guidance, class definitions, imagery dates (identical in every download) |

Benthic classes in these areas: Coral/Algae, Rock, Rubble, Sand, Seagrass.

**Map version and imagery dates** (from `Habitat-Map-Dates.pdf`, current as of 2022-12-13)

| Atlas region | Areas | Source imagery | Published |
| --- | --- | --- | --- |
| Eastern Tropical Pacific | Pacific coast and Isla del Coco | August 2018 to October 2020 | 2022-12-13 |
| Mesoamerica | Caribbean coast | August 2018 to July 2020 | 2022-07-19 |

**Read with care.** Coral/Algae means "any hardbottom area supporting living coral and/or algae" (Atlas class definitions). It does not separate live coral from algae or dead coral, and the maps predate the 2023 and 2024 bleaching. Describe sites as "coral or algae habitat according to the Allen Coral Atlas", not as live coral.

**License and citation.** Maps and statistics are © 2020 Allen Coral Atlas Partnership and Vulcan, Inc., licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Cite as:

> Allen Coral Atlas (2020). Imagery, maps and monitoring of the world's tropical coral reefs. doi.org/10.5281/zenodo.3833242

The satellite mosaic (Planet Labs, CC BY-NC-SA 4.0) was not downloaded and is not used.

## Candidate areas

Reviewed on 2026-11-06. Coral/Algae comes from `statistics.csv`. NOAA cells is an approximate count of the 0.05° Coral Reef Watch cells the Coral/Algae polygons touch; the exact water pixels are computed in F1-T01d.

| Area | Coast | Downloads | Coral/Algae (km²) | NOAA cells | Notes |
| --- | --- | --- | --- | --- | --- |
| `bahia-culebra` | Pacific north | 1 | 0.39 | 4 | Gulf of Papagayo, seasonal upwelling |
| `bahia-santa-elena` | Pacific north | 1 | 12.01 | 10 | Two coral clusters; may be split into two sites in F1-T01b |
| `cabo-blanco` | Pacific, Nicoya | 1 | 0.91 | 3 | Downloaded as "Cobalo"; Cabo Blanco and Cabuya |
| `curu-tambor-tortuga` | Pacific, Gulf of Nicoya | 2 | 1.57 | 8 | Curú, Pochote and Tambor merged with Isla Tortuga: they share a NOAA cell |
| `manuel-antonio` | Pacific central | 1 | 2.24 | 4 | |
| `uvita-bahia-ballena` | Pacific south | 1 | 0.70 | 4 | Uvita on the Pacific (Marino Ballena) |
| `isla-del-cano` | Pacific south | 1 | 0.49 | 2 | |
| `golfo-dulce-los-mogos` | Pacific south | 1 | 1.14 | 2 | Inner Golfo Dulce |
| `golfo-dulce-animas-dos-rios` | Pacific south | 1 | 1.19 | 5 | Ánimas, Dos Ríos and Bajo Mansito |
| `isla-del-coco` | Oceanic | 1 | 0.36 | 4 | |
| `limon-isla-uvita` | Caribbean | 1 | 0.18 | 2 | Coral around Isla Uvita, off Puerto Limón |
| `cahuita` | Caribbean | 1 | 2.12 | 3 | |
| `puerto-viejo-manzanillo` | Caribbean | 1 | 4.19 | 5 | Puerto Viejo, Chiquita, Manzanillo and Punta Mona |

**Discarded** (kept in `_discarded/` for traceability)

| Area | Reason |
| --- | --- |
| `mar-isla-del-coco` | Coral/Algae strip in open ocean about 16 km north-east of the island; likely an imagery artifact |
| `samara` | 0.02 km² of Coral/Algae |
| `conchal-brasilito-potrero` | 0.002 km² of Coral/Algae |
| `punta-banco` | Only reef extent; no benthic map |
| `san-pedrillo` | Only reef extent; no benthic map |

Working rule (proposed, confirmed in F1-T01e): an area needs a benthic map and at least 0.1 km² of Coral/Algae, and areas that share a NOAA cell are merged.
