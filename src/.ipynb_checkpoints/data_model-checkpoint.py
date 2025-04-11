"""Data models for the camera and user specification."""
from dataclasses import dataclass
import numpy as np

@dataclass
class Camera:
    fx: float
    fy: float
    cx: float
    cy: float
    sensor_size_x_mm: float
    sensor_size_y_mm: float
    image_size_x_px: int
    image_size_y_px: int

@dataclass
class DatasetSpec:
    """
    Data model for specifications of an image dataset.
    """
    overlap: float
    sidelap: float
    height: float
    scan_dimension_x: float
    scan_dimension_y: float
    exposure_time_ms: float


@dataclass
class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """
    pass