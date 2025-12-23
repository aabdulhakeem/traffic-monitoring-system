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

    # =========================
    # Main loop
    # =========================
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.track(frame)
        annotated_frame = frame.copy()

        # Draw counting area
        draw_area(annotated_frame, AREA)

        for r in results:
            if r.boxes.id is None:
                continue

            xyxys = r.boxes.xyxy.cpu().numpy()
            ids = r.boxes.id.cpu().numpy().astype(int)
            centers = compute_centers(xyxys)

            for (cx, cy), obj_id in zip(centers, ids):
                cx, cy = int(cx), int(cy)

                # Decide center color (inside / outside area)
                inside = point_inside_area(cx, cy, AREA)
                color = (0, 255, 0) if inside else (0, 0, 255)

                # Draw center point
                cv2.circle(
                    annotated_frame,
                    (cx, cy),
                    5,
                    color,
                    -1
                )

                # Draw object ID
                draw_text_with_bg(
                    annotated_frame,
                    text=str(obj_id),
                    x=cx + 10,
                    y=cy - 10,
                )

                # Area-based counting logic
                counter.process(obj_id, cx, cy)

        # Draw counters
        draw_overlay_info(
            annotated_frame,
            up_count=counter.up_count,
            down_count=counter.down_count,
        )

        cv2.imshow("Area-Based Vehicle Counting", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # =========================
    # Cleanup
    # =========================
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
