"""Tests for sites.grid (F1-T01c)."""

import pytest
from shapely.geometry import box

from sites.grid import pixel_center, pixel_of, pixels_touched


def test_example_from_the_learning_map() -> None:
    assert pixel_of(-85.6420, 10.58) == (1887, 1588)
    assert pixel_center((1887, 1588)) == (-85.625, 10.575)


def test_point_on_an_edge_goes_east_and_south() -> None:
    # -85.65 and 10.6 are exact cell edges
    assert pixel_center(pixel_of(-85.65, 10.6)) == (-85.625, 10.575)


def test_negative_longitudes_around_greenwich() -> None:
    assert pixel_center(pixel_of(-0.01, 0.01)) == (-0.025, 0.025)
    assert pixel_center(pixel_of(0.01, 0.01)) == (0.025, 0.025)


def test_coordinates_out_of_range_are_rejected() -> None:
    with pytest.raises(ValueError):
        pixel_of(180, 0)
    with pytest.raises(ValueError):
        pixel_of(0, -90)


def test_small_polygon_inside_one_cell() -> None:
    reef = box(-85.64, 10.58, -85.63, 10.59)
    assert pixels_touched(reef) == {(1887, 1588)}


def test_polygon_crossing_a_vertical_edge() -> None:
    reef = box(-85.66, 10.58, -85.64, 10.59)  # crosses lon -85.65
    assert pixels_touched(reef) == {(1886, 1588), (1887, 1588)}


def test_polygon_only_sharing_an_edge_counts_one_cell() -> None:
    reef = box(-85.66, 10.58, -85.65, 10.59)  # east side lies on lon -85.65
    assert pixels_touched(reef) == {(1886, 1588)}
