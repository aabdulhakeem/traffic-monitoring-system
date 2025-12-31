import cv2
import os
from datetime import datetime


def save_snapshot(frame, output_dir: str, prefix: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = f"{output_dir}/{prefix}_{timestamp}.jpg"

    cv2.imwrite(path, frame)
    return path
