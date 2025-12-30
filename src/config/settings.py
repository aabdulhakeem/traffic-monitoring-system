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

WRONG_WAY_VIDEO_PATH = os.getenv("WRONG_WAY_VIDEO_PATH")
if WRONG_WAY_VIDEO_PATH is None:
    raise ValueError("WRONG_WAY_VIDEO_PATH must be set in the .env file")


VIDEOS_OUTPUT_DIR = os.getenv("VIDEOS_OUTPUT_DIR", "output.mp4")
SNAPSHOTS_OUTPUT_DIR = os.getenv("SNAPSHOTS_OUTPUT_DIR", "snapshots")


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
ENTRY_LINE = np.array([[347, 596], [958, 596]])
EXIT_LINE = np.array([[155, 689], [897, 710]])

# Restricted area
RESTRICTED_AREA = np.array([
    [1, 492], 
    [469, 171], 
    [303, 133], 
    [3, 266]
    ])

VIDEO1_ROI_POLYGON = np.array([
    [361, 232], 
    [859, 237], 
    [1050, 320], 
    [1275, 547], 
    [1275, 709], 
    [9, 714], 
    [3, 12]
])

VIDEO2_ROI_POLYGON = np.array([
    [361, 580], 
    [1785, 453], 
    [1903, 968], 
    [5, 977], 
    [2, 733],
    ])


Point = Tuple[int, int]
Line = Tuple[Point, Point]

WINDOW_DURATION_SECONDS = 30  # 0.5 minute windows

VEHICLE_TYPES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}
