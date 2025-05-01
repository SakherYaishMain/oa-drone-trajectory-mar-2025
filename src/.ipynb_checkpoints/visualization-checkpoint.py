"""Utility to visualize photo plans.
"""

import typing as T

import plotly.graph_objects as go

from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans (T.List[Waypoint]): List of waypoints for the photo plan.

    Returns:
        go.Figure: Plotly figure object.
    """
    x_coords = [wp.x for wp in photo_plans]
    y_coords = [wp.y for wp in photo_plans]

    # Create scatter plot with lines to show the path
    fig = go.Figure()

    # Add the path line
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers',
        line=dict(color='blue'),
        marker=dict(size=6, color='red'),
        name='Waypoints'
    ))

    # Optionally, annotate with speed at a few points
    annotations = []
    for i in range(0, len(photo_plans), max(1, len(photo_plans) // 10)):
        wp = photo_plans[i]
        annotations.append(
            dict(
                x=wp.x,
                y=wp.y,
                text=f"{wp.speed:.2f} m/s",
                showarrow=True,
                arrowhead=1
            )
        )

    fig.update_layout(
        title="Drone Photo Plan (Top-Down View)",
        xaxis_title="X Position (meters)",
        yaxis_title="Y Position (meters)",
        annotations=annotations,
        width=800,
        height=600
    )

    return fig
