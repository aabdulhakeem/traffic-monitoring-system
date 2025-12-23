import cv2


def draw_overlay_info(frame, up_count, down_count):
    cv2.putText(
        frame, f"UP: {up_count}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )
    cv2.putText(
        frame, f"DOWN: {down_count}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
    )


def draw_area(frame, area):
    cv2.polylines(frame, [area], True, (255, 0, 255), 2)


def draw_text_with_bg(frame, text, x, y):
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
