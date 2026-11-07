"""Checks for data/sites/areas.csv (F1-T01b)."""

import csv
import json
from pathlib import Path

import pytest

from sites.bbox import _polygons

ROOT = Path(__file__).resolve().parents[2]
AREAS_CSV = ROOT / "data" / "sites" / "areas.csv"
RAW_ALLEN = ROOT / "data" / "raw" / "allen"
COASTS = {"pacific", "caribbean", "oceanic"}


def read_areas() -> list[dict[str, str]]:
    """Read every row of areas.csv as a dictionary."""
    with AREAS_CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def has_coral_inside(downloads: str, box: tuple[float, float, float, float]) -> bool:
    """True if any Coral/Algae vertex of the downloads falls inside the box."""
    min_lon, min_lat, max_lon, max_lat = box
    for download in downloads.split(";"):
        path = RAW_ALLEN / download / "Benthic-Map" / "benthic.geojson"
        data = json.loads(path.read_text(encoding="utf-8"))
        for feature in data["features"]:
            if feature["properties"]["class"] != "Coral/Algae":
                continue
            for polygon in _polygons(feature["geometry"]):
                for point in polygon[0]:
                    lon, lat = point[0], point[1]
                    if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                        return True
    return False


def test_slugs_are_unique() -> None:
    slugs = [row["slug"] for row in read_areas()]
    assert len(slugs) == len(set(slugs))


def test_coast_is_known() -> None:
    for row in read_areas():
        assert row["coast"] in COASTS, row["slug"]


def test_minimums_are_below_maximums() -> None:
    for row in read_areas():
        assert float(row["min_lon"]) < float(row["max_lon"]), row["slug"]
        assert float(row["min_lat"]) < float(row["max_lat"]), row["slug"]


@pytest.mark.data
@pytest.mark.skipif(not RAW_ALLEN.exists(), reason="needs data/raw/allen (not in Git)")
def test_every_box_contains_coral() -> None:
    for row in read_areas():
        box = (
            float(row["min_lon"]),
            float(row["min_lat"]),
            float(row["max_lon"]),
            float(row["max_lat"]),
        )
        assert has_coral_inside(row["downloads"], box), row["slug"]
