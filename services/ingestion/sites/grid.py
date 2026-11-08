"""NOAA Coral Reef Watch 0.05 degree grid (F1-T01c)."""

import math

from shapely.geometry import Polygon, box
from shapely.geometry.base import BaseGeometry

CELLS_PER_DEGREE = 20  # 1 / 0.5

type Pixel = tuple[int, int]  # (row, col) in the grid


def pixel_of(lon: float, lat: float) -> Pixel:
    """Return the (col, row) of the cell that contains the point.

    A point exactly on an edge belongs to the cell east of it and south of it.
    """
    if not (-180 <= lon < 180 and -90 < lat <= 90):
        raise ValueError(f"Longitude {lon} is out of range:({lon}, {lat})")

    col = math.floor(round((lon + 180) * CELLS_PER_DEGREE, 6))
    row = math.floor(round((90 - lat) * CELLS_PER_DEGREE, 6))

    return (col, row)


def pixel_center(pixel: Pixel) -> tuple[float, float]:
    """Return the (lon, lat) of the center of the cell."""
    col, row = pixel
    lon = -180 + (col + 0.5) / CELLS_PER_DEGREE
    lat = 90 - (row + 0.5) / CELLS_PER_DEGREE
    return (round(lon, 3), round(lat, 3))


def pixel_box(pixel: Pixel) -> Polygon:
    """Return the cell as  a rectangle (weest, sout, east, north)"""
    col, row = pixel
    size = 1 / CELLS_PER_DEGREE
    west = -180 + col / CELLS_PER_DEGREE
    north = 90 - row / CELLS_PER_DEGREE
    return box(west, north - size, west + size, north)


def pixels_touched(geometry: BaseGeometry) -> set[Pixel]:
    """Return every cell whose area overelaps the geometry

    A cell that only shares and edge with the geometry does not count
    """
    min_lon, min_lat, max_lon, max_lat = geometry.bounds
    first_col, first_row = pixel_of(min_lon, max_lat)
    last_col, last_row = pixel_of(max_lon, min_lat)

    touched = set()
    for col in range(first_col, last_col + 1):
        for row in range(first_row, last_row + 1):
            cell = pixel_box((col, row))
            if geometry.intersects(cell) and not geometry.touches(cell):
                touched.add((col, row))

    return touched
