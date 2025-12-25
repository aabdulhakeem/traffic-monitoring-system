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
CREATE TABLE IF NOT EXISTS area_violations (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,               -- camera or video
    vehicle_type TEXT NOT NULL,            -- car, bus, truck, motorcycle
    area_name TEXT NOT NULL,               -- restricted zone name

    violation_time TIMESTAMP NOT NULL,
    snapshot_path TEXT NOT NULL,           -- path to saved image

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 3. Wrong-Way Violations
-- =========================
CREATE TABLE IF NOT EXISTS wrong_way_violations (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,               -- camera or video
    vehicle_type TEXT NOT NULL,            -- car, bus, truck, motorcycle

    violation_time TIMESTAMP NOT NULL,
    snapshot_path TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

