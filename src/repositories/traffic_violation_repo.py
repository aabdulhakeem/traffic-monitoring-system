from datetime import datetime
from sqlalchemy import text


class TrafficViolationRepository:
    """
    Repository responsible for persisting traffic violations
    (restricted area, wrong way, etc.) into the database.
    """

    def __init__(self, db):
        self.db = db

    def insert(
        self,
        source_id: str,
        source_type: str,
        object_id: int,
        vehicle_type: str | None,
        violation_type: str,
        snapshot_path: str,
        violation_time: datetime,
    ):
        query = text("""
            INSERT INTO traffic_violations (
                source_id,
                source_type,
                object_id,
                vehicle_type,
                violation_type,
                snapshot_path,
                violation_time
            )
            VALUES (
                :source_id,
                :source_type,
                :object_id,
                :vehicle_type,
                :violation_type,
                :snapshot_path,
                :violation_time
            )
        """)

        self.db.execute(
            query,
            {
                "source_id": source_id,
                "source_type": source_type,
                "object_id": object_id,
                "vehicle_type": vehicle_type,
                "violation_type": violation_type,
                "snapshot_path": snapshot_path,
                "violation_time": violation_time,
            },
        )
        self.db.commit()