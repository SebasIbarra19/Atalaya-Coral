"""Coral habitat of each candidate area (F1-T01d, part A)."""

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import shapely
from shapely.geometry import box, shape
from shapely.geometry.base import BaseGeometry

from sites.bbox import BBox
from sites.grid import Pixel, pixels_touched

CORAL_CLASS = "Coral/Algae"


@dataclass(frozen=True)
class Area:
    """One row of areas.csv"""

    slug: str
    name: str
    coast: str
    downloads: tuple[str, ...]
    bbox: BBox
    active: bool = True
    note: str = ""


@dataclass(frozen=True)
class CoralSite:
    """A representative point on the coral of an area and the cells it covers"""

    slug: str
    lon: float
    lat: float
    pixels: tuple[Pixel, ...]


def parse_active(value: str) -> bool:
    """Turn the 'active' column into a bool, accepting only 'true' or 'false'."""
    if value not in ("true", "false"):
        raise ValueError(f"active must be 'true' or 'false', got {value!r}")
    return value == "true"


def read_areas(path: Path) -> list[Area]:
    """Read areas.csv and return a list of Area objects."""
    with path.open(encoding="utf-8") as f:
        return [
            Area(
                slug=row["slug"],
                name=row["name"],
                coast=row["coast"],
                downloads=tuple(row["downloads"].split(";")),
                bbox=(
                    float(row["min_lon"]),
                    float(row["min_lat"]),
                    float(row["max_lon"]),
                    float(row["max_lat"]),
                ),
                active=parse_active(row["active"]),
                note=row["note"],
            )
            for row in csv.DictReader(f)
        ]


def coral_geometry(area: Area, raw_dir: Path) -> BaseGeometry:
    """Return the union of the area's Coral/Algae polygons,
    clippled to its box.
    """
    shapes = []
    for download in area.downloads:
        path = raw_dir / download / "Benthic-Map" / "benthic.geojson"
        data = json.loads(path.read_text(encoding="utf-8"))

        for feature in data["features"]:
            if feature["properties"]["class"] == CORAL_CLASS:
                shapes.append(shapely.make_valid(shape(feature["geometry"])))

    if not shapes:
        raise ValueError(f"No {CORAL_CLASS} polygons found for {area.slug}")

    return shapely.union_all(shapes).intersection(box(*area.bbox))


def coral_site(area: Area, raw_dir: Path) -> CoralSite:
    """Return a representative point and the cells covered by the coral."""

    coral = coral_geometry(area, raw_dir)
    point = coral.representative_point()

    return CoralSite(
        slug=area.slug,
        lon=round(point.x, 4),
        lat=round(point.y, 4),
        pixels=tuple(sorted(pixels_touched(coral))),
    )
