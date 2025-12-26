from sqlalchemy import text
from datetime import datetime


class RestrictedAreaViolationRepository:
    def _init_(self, db):
        self.db = db

    def insert(
        self,
        source_id: str,
        source_type: str,
        object_id: int,
        vehicle_type: str,
        snapshot_path: str,
        violation_time: datetime,
    ):
        """
        Insert a restricted area violation event.
        """

        query = text("""
            INSERT INTO restricted_area_violations (
                source_id,
                source_type,
                object_id,
                vehicle_type,
                snapshot_path,
                violation_time
            )
            VALUES (
                :source_id,
                :source_type,
                :object_id,
                :vehicle_type,
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
                "snapshot_path": snapshot_path,
                "violation_time": violation_time,
            }
        )

        self.db.commit()