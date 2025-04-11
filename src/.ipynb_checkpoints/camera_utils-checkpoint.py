"""Utility functions for the camera model.
"""
import numpy as np

from src.data_model import Camera

def compute_focal_length_in_mm(camera: Camera) -> np.ndarray:
    """Computes the focal length in mm for the given camera

    Args:
        camera (Camera): the camera model.

    Returns:
        np.ndarray: [fx, fy] in mm.
    """
    raise NotImplementedError() 
    # Note(Ayush): Solution provided by project leader.
    # pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x_px
    # pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y_px

    # return np.array([camera.fx * pixel_to_mm_x, camera.fy * pixel_to_mm_y])

def project_world_point_to_image(camera: Camera, point: np.ndarray) -> np.ndarray:
    if point.shape != (3,):
        raise ValueError("Point must be a 3D vector (shape: (3,))")

    X, Y, Z = point

    if Z <= 0:
        raise ValueError("Point is behind the camera or on the image plane (Z must be > 0)")

    u = camera.fx * (X / Z) + camera.cx
    v = camera.fy * (Y / Z) + camera.cy

    return np.array([u, v])


def compute_image_footprint_on_surface(camera: Camera, distance_from_surface: float) -> np.ndarray:
    """Compute the footprint of the image captured by the camera at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).

    Returns:
        np.ndarray: [footprint_x, footprint_y] in meters.
    """

      # Convert pixel size to mm
    pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x_px
    pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y_px

    # Compute focal length in mm
    focal_length_mm_x = camera.fx * pixel_to_mm_x
    focal_length_mm_y = camera.fy * pixel_to_mm_y

    # Compute image footprint at given distance
    footprint_x = distance_from_surface * camera.sensor_size_x_mm / focal_length_mm_x
    footprint_y = distance_from_surface * camera.sensor_size_y_mm / focal_length_mm_y

    return np.array([footprint_x, footprint_y], dtype=np.float32)
    raise NotImplementedError()

def compute_ground_sampling_distance(camera: Camera, distance_from_surface: float) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).
    
    Returns:
        float: the GSD in meters (smaller among x and y directions).
    """
     # Reuse logic from compute_image_footprint_on_surface
    pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x_px
    pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y_px

    focal_length_mm_x = camera.fx * pixel_to_mm_x
    focal_length_mm_y = camera.fy * pixel_to_mm_y

    footprint_x_m = distance_from_surface * camera.sensor_size_x_mm / focal_length_mm_x
    footprint_y_m = distance_from_surface * camera.sensor_size_y_mm / focal_length_mm_y

    gsd_x = footprint_x_m / camera.image_size_x_px
    gsd_y = footprint_y_m / camera.image_size_y_px

    return min(gsd_x, gsd_y)
    raise NotImplementedError()
