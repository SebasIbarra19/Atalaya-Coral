import json
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
