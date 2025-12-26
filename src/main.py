import cv2

from config.settings import *

from vision.detect import VehicleDetector
from vision.geometry import compute_centers, point_inside_area
from vision.area_counter import AreaCounter
from utils.drawing import *


def main():
    # =========================
    # Initialize components
    # =========================
    detector = VehicleDetector(MODEL_PATH)
    counter = AreaCounter(
        area=AREA,
        area_top_y=AREA_TOP_Y,
        area_bottom_y=AREA_BOTTOM_Y,
    )

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {VIDEO_PATH}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        f"{OUTPUT_DIR}/vichle count.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.track(frame)
        annotated_frame = frame.copy()

        draw_area(annotated_frame, AREA)

        for r in results:
            if r.boxes.id is None:
                continue

            xyxys = r.boxes.xyxy.cpu().numpy()
            ids = r.boxes.id.cpu().numpy().astype(int)
            centers = compute_centers(xyxys)

            for (cx, cy), obj_id in zip(centers, ids):
                cx, cy = int(cx), int(cy)

                inside = point_inside_area(cx, cy, AREA)
                color = (0, 255, 0) if inside else (0, 0, 255)

                cv2.circle(annotated_frame, (cx, cy), 5, color, -1)

                draw_text_with_bg(
                    annotated_frame,
                    text=str(obj_id),
                    x=cx + 10,
                    y=cy - 10,
                )

                counter.process(obj_id, cx, cy)

        draw_overlay_info(
            annotated_frame,
            up_count=counter.up_count,
            down_count=counter.down_count,
        )

        out.write(annotated_frame)

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
