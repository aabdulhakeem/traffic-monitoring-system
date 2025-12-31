import cv2
from datetime import datetime

from src.config.settings import (
    VIDEO_PATH,
    VIDEOS_OUTPUT_DIR,
    SNAPSHOTS_OUTPUT_DIR,
    MODEL_PATH,
    RESTRICTED_AREA,
    VIDEO1_ROI_POLYGON as ROI,
    VEHICLE_TYPES,
)

from src.vision.detect import VehicleDetector
from src.vision.geometry import apply_polygon_mask, compute_centers, point_inside_area
from src.vision.restricted_area import RestrictedAreaMonitor
from src.utils.drawing import draw_area, draw_text_with_bg
from src.utils.snapshot import save_snapshot
from src.services.database import get_db
from src.services.email_service import EmailService
from src.repositories.traffic_violation_repo import TrafficViolationRepository


def main():
    # =========================
    # Initialization
    # =========================
    detector = VehicleDetector(MODEL_PATH)
    monitor = RestrictedAreaMonitor(RESTRICTED_AREA)

    db = next(get_db())
    repo = TrafficViolationRepository(db)
    email_service = EmailService()

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {VIDEO_PATH}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        f"{VIDEOS_OUTPUT_DIR}/restricted_area.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h),
    )

    # =========================
    # Video loop
    # =========================
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detected_frame = frame.copy()
        if ROI is not None:
            detected_frame = apply_polygon_mask(frame, ROI)
        results = detector.track(detected_frame)
        draw_area(frame, RESTRICTED_AREA)

        for r in results:
            if r.boxes.id is None:
                continue

            centers = compute_centers(r.boxes.xyxy.cpu().numpy())
            ids = r.boxes.id.cpu().numpy().astype(int)
            vehicle_types = r.boxes.cls.cpu().numpy().astype(int)
            vehicle_types = [VEHICLE_TYPES.get(vt, "unknown") for vt in vehicle_types]

            for (cx, cy), obj_id, v_type in zip(centers, ids, vehicle_types):
                violated = monitor.process(obj_id, int(cx), int(cy))

                if violated:
                    snapshot = save_snapshot(
                        frame,
                        output_dir=f"{SNAPSHOTS_OUTPUT_DIR}",
                        prefix="restricted_area",
                    )

                    repo.insert(
                        source_id="video_1",
                        source_type="video",
                        object_id=int(obj_id),
                        vehicle_type=v_type,
                        violation_type="restricted_area",
                        snapshot_path=snapshot,
                        violation_time=datetime.now(),
                    )

                    email_service.send_violation_alert(
                        title="🚨 Restricted Area Violation",
                        body=f"team 2: Vehicle {obj_id} ({v_type}) entered a restricted area.",
                        snapshot_path=snapshot,
                    )

        out.write(frame)

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
