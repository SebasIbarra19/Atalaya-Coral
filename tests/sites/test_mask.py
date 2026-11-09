"""Tests for sites.mask (F1-T01d, part B). No network: answers are written by hand."""

from sites.mask import mask_url, parse_mask_csv

ANSWER = """time,latitude,longitude,CRW_DHW_mask
UTC,degrees_north,degrees_east,1
2026-01-01T12:00:00Z,10.575,-85.625,0
2026-01-01T12:00:00Z,10.575,-85.575,1
2026-01-01T12:00:00Z,10.525,-85.625,NaN
"""


def test_url_asks_for_the_box_of_cell_centers() -> None:
    url = mask_url("https://example.org/erddap/", {(1887, 1588), (1888, 1589)})
    assert url.startswith("https://example.org/erddap/griddap/dhw_5km.csv?CRW_DHW_mask")
    assert "%5B(10.525):1:(10.575)%5D" in url
    assert "%5B(-85.625):1:(-85.575)%5D" in url


def test_answer_is_read_into_flags_per_cell() -> None:
    assert parse_mask_csv(ANSWER) == {(1887, 1588): 0, (1888, 1588): 1}
