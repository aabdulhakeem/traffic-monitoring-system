import cv2
from datetime import datetime, timedelta

from src.config.settings import (
    VIDEO_PATH,
    VIDEOS_OUTPUT_DIR,
    MODEL_PATH,
    AREA,
    WINDOW_DURATION_SECONDS,
    VIDEO1_ROI_POLYGON as ROI,
)

from src.vision.detect import VehicleDetector
from src.vision.geometry import apply_polygon_mask, compute_centers, point_inside_area
from src.vision.area_counter import AreaCounter
from src.utils.drawing import draw_area, draw_overlay_info, draw_text_with_bg
from src.services.database import get_db
from src.repositories.traffic_count_repo import TrafficCountRepository


def main():

    detector = VehicleDetector(MODEL_PATH)
    counter = AreaCounter(
        area=AREA,
        area_top_y=AREA[:, 1].max(),
        area_bottom_y=AREA[:, 1].min(),
    )

    db = next(get_db())
    repo = TrafficCountRepository(db)

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {VIDEO_PATH}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_per_window = int(fps * WINDOW_DURATION_SECONDS)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        f"{VIDEOS_OUTPUT_DIR}/vehicle_counting.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h),
    )

    # =========================
    # Window tracking
    # =========================
    frame_count = 0
    window_start_time = datetime.now()

    up_count_prev = 0
    down_count_prev = 0

    # =========================
    # Video loop
    # =========================
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        
        detected_frame = frame.copy()
        if ROI is not None:
            detected_frame = apply_polygon_mask(frame, ROI)
        results = detector.track(detected_frame)
        draw_area(frame, AREA)

        for r in results:
            if r.boxes.id is None:
                continue

            centers = compute_centers(r.boxes.xyxy.cpu().numpy())
            ids = r.boxes.id.cpu().numpy().astype(int)

            for (cx, cy), obj_id in zip(centers, ids):
                counter.process(obj_id, int(cx), int(cy))

        draw_overlay_info(frame, counter.up_count, counter.down_count)

        out.write(frame)


        # =========================
        # Window end
        # =========================
        if frame_count % frames_per_window == 0:
            window_end_time = datetime.now()

            repo.insert(
                source_id="video_1",
                source_type="video",
                window_start=window_start_time,
                window_end=window_end_time,
                up_count=counter.up_count - up_count_prev,
                down_count=counter.down_count - down_count_prev,
            )

            # Prepare next window
            up_count_prev = counter.up_count
            down_count_prev = counter.down_count
            window_start_time = window_end_time

    # =========================
    # Save remaining window
    # =========================
    if counter.up_count != up_count_prev or counter.down_count != down_count_prev:
        repo.insert(
            source_id="video_1",
            source_type="video",
            window_start=window_start_time,
            window_end=datetime.now(),
            up_count=counter.up_count - up_count_prev,
            down_count=counter.down_count - down_count_prev,
        )

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
