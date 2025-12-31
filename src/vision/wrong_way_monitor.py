from typing import Dict, Set, Tuple
from src.config.settings import Line
from src.vision.geometry import has_crossed_line


class WrongWayMonitor:
    """
    Detects wrong-way driving by tracking the order in which
    a vehicle crosses entry and exit lines.

    Correct direction:
        entry_line -> exit_line

    Wrong direction:
        exit_line -> entry_line
    """

    def __init__(
        self,
        entry_line: Line,
        exit_line: Line,
        allowed_direction: str = "entry_to_exit",
    ):
        """
        entry_line: ((x1, y1), (x2, y2))
        exit_line:  ((x1, y1), (x2, y2))
        allowed_direction:
            - "entry_to_exit" (default)
            - "exit_to_entry"
        """
        self.entry_line = entry_line
        self.exit_line = exit_line
        self.allowed_direction = allowed_direction

        # obj_id -> "entry" | "exit"
        self.first_cross: Dict[int, str] = {}

        # Vehicles already reported as violations
        self.violated_ids: Set[int] = set()

        # Last known center for each object
        self.last_centers: Dict[int, Tuple[int, int]] = {}

    # =========================
    # Main logic
    # =========================
    def process(self, obj_id: int, cx: int, cy: int) -> bool:
        """
        Process a tracked object center.

        Returns True if a NEW wrong-way violation is detected.
        """
        current_center = (cx, cy)

        # First time seeing this object
        if obj_id not in self.last_centers:
            self.last_centers[obj_id] = current_center
            return False

        prev_center = self.last_centers[obj_id]

        crossed_entry = has_crossed_line(
            prev_center, current_center, self.entry_line
        )
        crossed_exit = has_crossed_line(
            prev_center, current_center, self.exit_line
        )

        # Record first crossing
        if crossed_entry and obj_id not in self.first_cross:
            self.first_cross[obj_id] = "entry"

        elif crossed_exit and obj_id not in self.first_cross:
            self.first_cross[obj_id] = "exit"

        # Second crossing → decide direction
        elif crossed_entry or crossed_exit:
            if obj_id in self.violated_ids:
                self.last_centers[obj_id] = current_center
                return False

            first = self.first_cross.get(obj_id)

            if self.allowed_direction == "entry_to_exit":
                wrong = first == "exit" and crossed_entry
            else:
                wrong = first == "entry" and crossed_exit

            if wrong:
                self.violated_ids.add(obj_id)
                self.last_centers[obj_id] = current_center
                return True

        self.last_centers[obj_id] = current_center
        return False
