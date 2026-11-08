"""Tests for sites.coral (F1-T01d, part A)."""

import json
from pathlib import Path

import pytest
from shapely.geometry import Point, box, mapping

from sites.coral import Area, coral_geometry, coral_site, read_areas

ROOT = Path(__file__).resolve().parents[2]
RAW_ALLEN = ROOT / "data" / "raw" / "allen"

# Both squares live in the cell of the learning-map example: col 1887, row 1588
CORAL = box(-85.64, 10.58, -85.63, 10.59)
SAND = box(-85.62, 10.58, -85.61, 10.59)
WHOLE_CELL = (-85.65, 10.55, -85.60, 10.60)


def write_download(
    raw_dir: Path, download: str, features: list[tuple[str, object]]
) -> None:
    """Write a fake Atlas download with (class, shapely geometry) features."""
    path = raw_dir / download / "Benthic-Map" / "benthic.geojson"
    path.parent.mkdir(parents=True)
    data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"class": c}, "geometry": mapping(g)}
            for c, g in features
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def make_area(downloads: tuple[str, ...], bbox=WHOLE_CELL) -> Area:
    return Area(
        slug="test", name="Test", coast="pacific", downloads=downloads, bbox=bbox
    )


def test_only_coral_is_kept(tmp_path: Path) -> None:
    write_download(tmp_path, "a/dl", [("Coral/Algae", CORAL), ("Sand", SAND)])
    coral = coral_geometry(make_area(("a/dl",)), tmp_path)
    assert coral.area == pytest.approx(CORAL.area)


def test_coral_is_clipped_to_the_box(tmp_path: Path) -> None:
    write_download(tmp_path, "a/dl", [("Coral/Algae", CORAL)])
    half = (-85.65, 10.55, -85.635, 10.60)  # cuts the coral square in half
    coral = coral_geometry(make_area(("a/dl",), half), tmp_path)
    assert coral.area == pytest.approx(CORAL.area / 2)


def test_every_download_of_a_merged_area_is_read(tmp_path: Path) -> None:
    west = box(-85.69, 10.58, -85.68, 10.59)  # one cell to the west: col 1886
    write_download(tmp_path, "a/east", [("Coral/Algae", CORAL)])
    write_download(tmp_path, "a/west", [("Coral/Algae", west)])
    area = make_area(("a/east", "a/west"), (-85.70, 10.55, -85.60, 10.60))
    assert coral_site(area, tmp_path).pixels == ((1886, 1588), (1887, 1588))


def test_site_point_is_on_the_coral_with_four_decimals(tmp_path: Path) -> None:
    write_download(tmp_path, "a/dl", [("Coral/Algae", CORAL), ("Sand", SAND)])
    site = coral_site(make_area(("a/dl",)), tmp_path)
    assert CORAL.contains(Point(site.lon, site.lat))
    assert round(site.lon, 4) == site.lon and round(site.lat, 4) == site.lat
    assert site.pixels == ((1887, 1588),)


def test_area_without_coral_is_rejected(tmp_path: Path) -> None:
    write_download(tmp_path, "a/dl", [("Sand", SAND)])
    with pytest.raises(ValueError, match="No Coral/Algae"):
        coral_geometry(make_area(("a/dl",)), tmp_path)


@pytest.mark.data
@pytest.mark.skipif(not RAW_ALLEN.exists(), reason="needs data/raw/allen (not in Git)")
def test_every_real_site_sits_on_coral() -> None:
    for area in read_areas(ROOT / "data" / "sites" / "areas.csv"):
        coral = coral_geometry(area, RAW_ALLEN)
        site = coral_site(area, RAW_ALLEN)
        assert coral.contains(Point(site.lon, site.lat)), area.slug
        assert site.pixels, area.slug
