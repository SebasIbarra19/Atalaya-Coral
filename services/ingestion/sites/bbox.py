import json
import math
from pathlib import Path

type BBox = tuple[float, float, float, float]


def _polygons(geometry: dict) -> list:
    """return the geometry as a list of polygons, each one as a list of rings"""

    kind = geometry["type"]

    if kind == "Polygon":
        return [geometry["coordinates"]]
    if kind == "MultiPolygon":
        return geometry["coordinates"]

    raise ValueError(f"Expected Polygon or MultiPolygon, got {kind}")


def bbox_from_geojson(path: Path) -> BBox:
    """Return (min_lon, min_lat, max_lon, max_lat)
    over the exterior rings of every feature."""

    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    lons: list[float] = []
    lats: list[float] = []

    for feature in data["features"]:
        for polygon in _polygons(feature["geometry"]):
            exterior = polygon[0]
            for point in exterior:
                lons.append(point[0])
                lats.append(point[1])

    if not lons:
        raise ValueError(f"No polygon coordinates found in {path}")

    return (min(lons), min(lats), max(lons), max(lats))


def round_outward(bbox: BBox, decimals: int = 4) -> BBox:
    """Round the coordinates of a bounding box outward to the given
    number of decimals, so the box never shrinks."""

    factor = 10**decimals
    min_lon, min_lat, max_lon, max_lat = bbox
    return (
        math.floor(round(min_lon * factor, 6)) / factor,
        math.floor(round(min_lat * factor, 6)) / factor,
        math.ceil(round(max_lon * factor, 6)) / factor,
        math.ceil(round(max_lat * factor, 6)) / factor,
    )


def union_bbox(a: BBox, b: BBox) -> BBox:
    """Return the smallest box that contains both boxes."""
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
