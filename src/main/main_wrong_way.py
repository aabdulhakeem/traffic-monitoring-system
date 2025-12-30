import cv2
from datetime import datetime

from src.config.settings import (
    WRONG_WAY_VIDEO_PATH as VIDEO_PATH,
    SNAPSHOTS_OUTPUT_DIR,
    VIDEOS_OUTPUT_DIR,
    MODEL_PATH,
    ENTRY_LINE,
    EXIT_LINE,
    VIDEO2_ROI_POLYGON as ROI,
    VEHICLE_TYPES,
)

from src.vision.detect import VehicleDetector
from src.vision.geometry import apply_polygon_mask, compute_centers
from src.vision.wrong_way_monitor import WrongWayMonitor
from src.utils.drawing import (
    draw_line,
    draw_direction_arrow,
    draw_text_with_bg,
)
from src.utils.snapshot import save_snapshot
from src.services.database import get_db
from src.services.email_service import EmailService
from src.repositories.traffic_violation_repo import TrafficViolationRepository


def main():
    # =========================
    # Initialization
    # =========================
    detector = VehicleDetector(MODEL_PATH)
    monitor = WrongWayMonitor(
        entry_line=ENTRY_LINE,
        exit_line=EXIT_LINE,
    )

    db = next(get_db())
    repo = TrafficViolationRepository(db)
    email_service = EmailService()

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {VIDEO_PATH}")
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

        for r in results:
            if r.boxes.id is None:
                continue

            centers = compute_centers(r.boxes.xyxy.cpu().numpy())
            ids = r.boxes.id.cpu().numpy().astype(int)
            vehicle_types = r.boxes.cls.cpu().numpy().astype(int)
            vehicle_types = [VEHICLE_TYPES.get(vt, "unknown") for vt in vehicle_types]


            for (cx, cy), obj_id, vehicle_type in zip(centers, ids, vehicle_types):
                cx, cy = int(cx), int(cy)
                obj_id = int(obj_id)

                violated = monitor.process(obj_id, cx, cy)
                # =========================
                # Violation handling
                # =========================
                if violated:
                    snapshot_path = save_snapshot(
                        frame,
                        output_dir=f"{SNAPSHOTS_OUTPUT_DIR}",
                        prefix="wrong_way",
                    )

                    repo.insert(
                        source_id="video_2",
                        source_type="video",
                        object_id=obj_id,
                        vehicle_type=vehicle_type,
                        violation_type="wrong_way",
                        snapshot_path=snapshot_path,
                        violation_time=datetime.now(),
                    )

                    email_service.send_violation_alert(
                        title="🚨 Wrong Way Detected",
                        body=f"team 2: Vehicle {obj_id} ({vehicle_type}) entered a restricted area.",
                        snapshot_path=snapshot_path,
                    )

    cap.release()

if __name__ == "__main__":
    main()
