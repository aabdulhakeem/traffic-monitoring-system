import cv2
from typing import Tuple
from config.settings import Point, Line

# =========================
# Overlay text
# =========================
def draw_text_with_bg(frame, text: str, x: int, y: int):
    (w, h), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
    )

    cv2.rectangle(
        frame,
        (x - 4, y - h - 4),
        (x + w + 4, y + baseline + 4),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


# =========================
# Draw counters
# =========================
def draw_overlay_info(frame, up_count: int, down_count: int):
    cv2.putText(
        frame,
        f"UP: {up_count}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )
    cv2.putText(
        frame,
        f"DOWN: {down_count}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )


# =========================
# Draw areas
# =========================
def draw_area(frame, area):
    """
    Draw polygon area (restricted / counting).
    """
    cv2.polylines(frame, [area], True, (255, 0, 255), 2)


# =========================
# Draw lines (Wrong Way)
# =========================
def draw_line(
    frame,
    line: Line,
    color=(0, 255, 255),
    thickness: int = 2,
    label: str | None = None,
):
    """
    Draw a single line with optional label.
    """
    (x1, y1), (x2, y2) = line
    cv2.line(frame, (x1, y1), (x2, y2), color, thickness)

    if label:
        draw_text_with_bg(frame, label, x1 + 5, y1 - 5)


def draw_direction_arrow(
    frame,
    start: Point,
    end: Point,
    color=(0, 255, 0),
    thickness: int = 2,
):
    """
    Draw an arrow indicating allowed direction.
    """
    cv2.arrowedLine(
        frame,
        start,
        end,
        color,
        thickness,
        tipLength=0.25
    )