"""Tests for sites.bbox (F1-T01b)."""

import json
from pathlib import Path

import pytest

from sites.bbox import bbox_from_geojson

SQUARE = [[[-85.0, 9.0], [-84.9, 9.0], [-84.9, 9.1], [-85.0, 9.1], [-85.0, 9.0]]]


def write_geojson(path: Path, geometry: dict) -> Path:
    """Write a FeatureCollection with one feature and return its path."""
    data = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {}, "geometry": geometry}],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_polygon(tmp_path: Path) -> None:
    geometry = {"type": "Polygon", "coordinates": SQUARE}
    path = write_geojson(tmp_path / "area.geojson", geometry)
    assert bbox_from_geojson(path) == (-85.0, 9.0, -84.9, 9.1)


def test_multipolygon_covers_every_part(tmp_path: Path) -> None:
    far = [[[-84.0, 10.0], [-83.9, 10.0], [-83.9, 10.0], [-83.9, 10.1], [-84.0, 10.0]]]
    geometry = {"type": "MultiPolygon", "coordinates": [SQUARE, far]}
    path = write_geojson(tmp_path / "area.geojson", geometry)
    assert bbox_from_geojson(path) == (-85.0, 9.0, -83.9, 10.1)


def test_point_with_altitude(tmp_path: Path) -> None:
    ring = [[-85.0, 9.0, 0.0], [-84.9, 9.0, 0.0], [-84.9, 9.1, 0.0], [-85.0, 9.0, 0.0]]
    geometry = {"type": "Polygon", "coordinates": [ring]}
    path = write_geojson(tmp_path / "area.geojson", geometry)
    assert bbox_from_geojson(path) == (-85.0, 9.0, -84.9, 9.1)


def test_other_geometry_types_are_rejected(tmp_path: Path) -> None:
    geometry = {"type": "Point", "coordinates": [-85.0, 9.0]}
    path = write_geojson(tmp_path / "point.json", geometry)
    with pytest.raises(ValueError, match="Point"):
        bbox_from_geojson(path)
