"""Tests for the cell choice in sites.build (F1-T01d, part B)."""

from sites.build import choose_cells, format_cells
from sites.grid import with_neighbors

CORAL_CELLS = {(1887, 1588), (1888, 1588)}


def test_neighbors_include_diagonals() -> None:
    assert len(with_neighbors({(10, 10)})) == 9
    assert len(with_neighbors({(10, 10), (11, 10)})) == 12


def test_water_cells_under_the_coral_are_kept() -> None:
    flags = {(1887, 1588): 0, (1888, 1588): 1}
    assert choose_cells(CORAL_CELLS, flags) == ([(1887, 1588)], "coral")


def test_neighbors_are_used_when_the_coral_cells_are_land() -> None:
    flags = {(1887, 1588): 1, (1888, 1588): 1, (1887, 1589): 0}
    assert choose_cells(CORAL_CELLS, flags) == ([(1887, 1589)], "neighbors")


def test_no_water_at_all_is_reported() -> None:
    assert choose_cells(CORAL_CELLS, {}) == ([], "none")


def test_cells_are_written_as_centers() -> None:
    assert format_cells([(1887, 1588), (1888, 1588)]) == "-85.625 10.575;-85.575 10.575"
