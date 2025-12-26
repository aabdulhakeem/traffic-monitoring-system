-- =========================
-- 1. Vehicle Counting (Time-window based)
-- =========================
CREATE TABLE IF NOT EXISTS traffic_counts (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,              -- camera_id or video_id
    source_type TEXT NOT NULL,            -- 'video' | 'live_camera'

    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,

    up_count INTEGER NOT NULL CHECK (up_count >= 0),
    down_count INTEGER NOT NULL CHECK (down_count >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 2. Restricted Area Violations
-- =========================
CREATE TABLE IF NOT EXISTS restricted_area_violations (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL,

    object_id INTEGER NOT NULL,
    vehicle_type TEXT,

    snapshot_path TEXT NOT NULL,

    violation_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 3. Wrong-Way Violations
-- =========================
CREATE TABLE IF NOT EXISTS wrong_way_violations (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL,

    object_id INTEGER NOT NULL,
    vehicle_type TEXT,

    entry_line_id TEXT,
    exit_line_id TEXT,

    snapshot_path TEXT NOT NULL,

    violation_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);