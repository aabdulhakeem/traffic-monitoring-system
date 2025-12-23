from ultralytics import YOLO


class VehicleDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def track(self, frame):
        return self.model.track(
            # car, motorbike, bus, truck
            frame, persist=True, classes=[2, 3, 5, 7]
        )
