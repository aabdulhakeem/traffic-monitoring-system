from sqlalchemy import text
from datetime import datetime


class TrafficCountRepository:
    def __init__(self, db):
        """
        db: SQLAlchemy session
        """
        self.db = db

    def insert(
        self,
        source_id: str,
        source_type: str,
        window_start: datetime,
        window_end: datetime,
        up_count: int,
        down_count: int,
    ):
        """
        Insert traffic counting data for a specific time window.
        """

        query = text("""
            INSERT INTO traffic_counts (
                source_id,
                source_type,
                window_start,
                window_end,
                up_count,
                down_count
            )
            VALUES (
                :source_id,
                :source_type,
                :window_start,
                :window_end,
                :up_count,
                :down_count
            )
        """)

        self.db.execute(
            query,
            {
                "source_id": source_id,
                "source_type": source_type,
                "window_start": window_start,
                "window_end": window_end,
                "up_count": up_count,
                "down_count": down_count,
            }
        )

        self.db.commit()
