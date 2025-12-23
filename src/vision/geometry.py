import cv2
import numpy as np

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
