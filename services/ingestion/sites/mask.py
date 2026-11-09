"""Water and land flags of the NOAA grid, read from ERDDAP (F1-T01d, part B)."""

import csv
import io
import urllib.parse
import urllib.request

from sites.grid import Pixel, pixel_center, pixel_of

DATASET = "dhw_5km"
MASK_VARIABLE = "CRW_DHW_mask"
MASK_DATE = "2026-01-01T12:00:00Z"
WATER = 0


def mask_url(base_url: str, pixels: set[Pixel]) -> str:
    """Return the griddap URL for the mask of every cell in the pixels' box."""
    centers = [pixel_center(p) for p in pixels]
    lons = [lon for lon, _ in centers]
    lats = [lat for _, lat in centers]

    query = (
        f"{MASK_VARIABLE}[({MASK_DATE})]"
        f"[({min(lats)}):1:({max(lats)})]"
        f"[({min(lons)}):1:({max(lons)})]"
    )
    safe = urllib.parse.quote(query, safe="():,.-_")
    return f"{base_url.rstrip('/')}/griddap/{DATASET}.csv?{safe}"


def parse_mask_csv(text: str) -> dict[Pixel, int]:
    """Return ERDDAP's .csv answer (names, units, then rows) into a flag per cell"""
    rows = list(csv.reader(io.StringIO(text)))
    header = rows[0]
    i_lat = header.index("latitude")
    i_lon = header.index("longitude")
    i_mask = header.index(MASK_VARIABLE)
    flags: dict[Pixel, int] = {}

    for row in rows[2:]:
        try:
            flag = int(float(row[i_mask]))
        except ValueError:
            continue  # NaN or empty: no information, so not water
        flags[pixel_of(float(row[i_lon]), float(row[i_lat]))] = flag
    return flags


def fetch_mask(
    base_url: str, pixels: set[Pixel], timeout: float = 60
) -> dict[Pixel, int]:
    """Download the mask of the pixel's box from ERDDAP"""
    with urllib.request.urlopen(
        mask_url(base_url, pixels), timeout=timeout
    ) as response:
        return parse_mask_csv(response.read().decode("utf-8"))
