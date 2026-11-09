"""Build data/sites/sites.csv from areas, Atlas coral and NOAA mask (F1-T01d)."""

import csv
import os
from pathlib import Path

from sites.coral import coral_site, read_areas
from sites.grid import Pixel, pixel_center, with_neighbors
from sites.mask import WATER, fetch_mask

ROOT = Path(__file__).resolve().parents[3]
AREAS_CSV = ROOT / "data" / "sites" / "areas.csv"
SITES_CSV = ROOT / "data" / "sites" / "sites.csv"
RAW_ALLEN = ROOT / "data" / "raw" / "allen"
COLUMNS = ["slug", "name", "coast", "lon", "lat", "coral_cells", "cells_from", "cells"]


def choose_cells(
    candidates: set[Pixel], flags: dict[Pixel, int]
) -> tuple[list[Pixel], str]:
    """Keep the water cells under the coral, or else the water cells around it"""
    under = sorted(p for p in candidates if flags.get(p) == WATER)
    if under:
        return under, "coral"

    around = sorted(
        p for p in with_neighbors(candidates) - candidates if flags.get(p) == WATER
    )
    if around:
        return around, "neighbors"

    return [], "none"


def format_cells(cells: list[Pixel]) -> str:
    """Write cell centers as 'lon lat' pairs separated by ';'."""
    return ";".join(f"{lon:.3f} {lat:.3f}" for lon, lat in map(pixel_center, cells))


def main() -> None:
    base_url = os.environ.get("ERDDAP_BASE_URL")
    if not base_url:
        raise SystemExit("ERDDAP_BASE_URL env variable is not set (see .env.example)")

    rows = []
    for area in read_areas(AREAS_CSV):
        site = coral_site(area, RAW_ALLEN)
        candidates = set(site.pixels)
        flags = fetch_mask(base_url, with_neighbors(candidates))
        cells, cells_from = choose_cells(candidates, flags)
        print(f"{area.slug}: {len(cells)} water cells ({cells_from})")

        rows.append(
            {
                "slug": area.slug,
                "name": area.name,
                "coast": area.coast,
                "lon": f"{site.lon:.4f}",
                "lat": f"{site.lat:.4f}",
                "coral_cells": len(site.pixels),
                "cells_from": cells_from,
                "cells": format_cells(cells),
            }
        )
    with SITES_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} sites to {SITES_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
