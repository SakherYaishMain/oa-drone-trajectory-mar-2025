import typing as T
import math

import numpy as np

from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import compute_image_footprint_on_surface, compute_ground_sampling_distance


def compute_distance_between_images(camera: Camera, dataset_spec: DatasetSpec) -> np.ndarray:
    """Compute the distance between images in the horizontal and vertical directions for specified overlap and sidelap.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        float: The distance between images in the horizontal direction.
        float: The distance between images in the vertical direction.
    """
    # Step 1: Compute image footprint at the given height
    footprint_x, footprint_y = compute_image_footprint_on_surface(camera, dataset_spec.height)

    # Step 2: Compute distances based on overlap and sidelap
    horizontal_distance = footprint_x * (1 - dataset_spec.overlap)
    vertical_distance = footprint_y * (1 - dataset_spec.sidelap)

    return np.array([horizontal_distance, vertical_distance], dtype=np.float32)
    raise NotImplementedError()


def compute_speed_during_photo_capture(camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1) -> float:
    """Compute the speed of drone during an active photo capture to prevent more than 1px of motion blur.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.
        allowed_movement_px (float, optional): The maximum allowed movement in pixels. Defaults to 1 px.

    Returns:
        float: The speed at which the drone should move during photo capture.
    """
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)  # in meters per pixel
    exposure_time_sec = dataset_spec.exposure_time_ms / 1000  # convert ms to seconds

    speed = gsd * allowed_movement_px / exposure_time_sec
    return speed


def generate_photo_plan_on_grid(camera: Camera, dataset_spec: DatasetSpec) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        List[Waypoint]: scan plan as a list of waypoints.

    """
    distance_x, distance_y = compute_distance_between_images(camera, dataset_spec)

    num_cols = math.ceil(dataset_spec.scan_dimension_x / distance_x)
    num_rows = math.ceil(dataset_spec.scan_dimension_y / distance_y)

    speed = compute_speed_during_photo_capture(camera, dataset_spec)

    waypoints = []
    for row in range(num_rows):
        y = row * distance_y
        row_waypoints = []

        for col in range(num_cols):
            x = col * distance_x
            row_waypoints.append(Waypoint(x=x, y=y, z=dataset_spec.height, speed=speed))

        # Reverse direction every other row for lawn-mower pattern
        if row % 2 == 1:
            row_waypoints.reverse()

        waypoints.extend(row_waypoints)

    return waypoints

