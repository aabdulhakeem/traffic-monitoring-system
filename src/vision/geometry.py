import cv2
import numpy as np
from typing import Tuple
from src.config.settings import Point, Line

def point_inside_area(x: int, y: int, area: np.ndarray) -> bool:
    """
    Check whether a point lies inside a polygonal area.
    """
    return cv2.pointPolygonTest(area, (x, y), False) >= 0


def compute_centers(xyxys: np.ndarray) -> np.ndarray:
    """
    Compute center points from bounding boxes.
    """
    return np.column_stack((
        (xyxys[:, 0] + xyxys[:, 2]) // 2,
        (xyxys[:, 1] + xyxys[:, 3]) // 2
    ))


def has_crossed_line(
    prev_point: Point,
    curr_point: Point,
    line: Line
) -> bool:
    """
    Returns True if the point crossed the line
    between two consecutive frames.
    """

    def side_of_line(p: Point, l: Line) -> float:
        (x, y) = p
        (x1, y1), (x2, y2) = l
        return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)

    prev_side = side_of_line(prev_point, line)
    curr_side = side_of_line(curr_point, line)

    return prev_side * curr_side < 0
