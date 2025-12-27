import os
import numpy as np
from dotenv import load_dotenv
from typing import Tuple
# Load environment variables from .env
load_dotenv()


# =========================
# Runtime configuration
# =========================

VIDEO_PATH = os.getenv("VIDEO_PATH")
if VIDEO_PATH is None:
    raise ValueError("VIDEO_PATH must be set in the .env file")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output.mp4")

# YOLO v11 default model (can be overridden via .env)
MODEL_PATH = os.getenv("MODEL_PATH", "yolo11n.pt")

# =========================
# Database configuration
# =========================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =========================
# Email configuration
# =========================
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")

# =========================
# Scene configuration
# =========================

# Area used for area-based vehicle counting
AREA = np.array([
    [96, 475],
    [1189, 475],
    [1110, 394],
    [165, 394]
])

# Reference Y-coordinates for entry/exit logic
AREA_TOP_Y = 494
AREA_BOTTOM_Y = 475

# Restricted area
RESTRICTED_AREA = np.array([
    (112, 388),
    (395, 377),
    (343, 453),
    (90, 453)
])

Point = Tuple[int, int]
Line = Tuple[Point, Point]
