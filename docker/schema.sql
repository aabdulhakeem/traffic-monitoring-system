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

CREATE TABLE IF NOT EXISTS traffic_violations (
    id SERIAL PRIMARY KEY,

    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL,

    object_id INTEGER NOT NULL,
    vehicle_type TEXT,

    violation_type TEXT NOT NULL,
    -- 'restricted_area' | 'wrong_way'

    snapshot_path TEXT NOT NULL,
    violation_time TIMESTAMP NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- =========================