from sqlalchemy import text
from datetime import datetime


class WrongWayViolationRepository:
    def _init_(self, db):
        self.db = db

    def insert(
        self,
        source_id: str,
        source_type: str,
        object_id: int,
        vehicle_type: str,
        entry_line_id: str,
        exit_line_id: str,
        snapshot_path: str,
        violation_time: datetime,
    ):
        """
        Insert a wrong-way driving violation event.
        """

        query = text("""
            INSERT INTO wrong_way_violations (
                source_id,
                source_type,
                object_id,
                vehicle_type,
                entry_line_id,
                exit_line_id,
                snapshot_path,
                violation_time
            )
            VALUES (
                :source_id,
                :source_type,
                :object_id,
                :vehicle_type,
                :entry_line_id,
                :exit_line_id,
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
                "entry_line_id": entry_line_id,
                "exit_line_id": exit_line_id,
                "snapshot_path": snapshot_path,
                "violation_time": violation_time,
            }
        )

        self.db.commit()