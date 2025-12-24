from vision.geometry import point_inside_area

class RestrictedAreaMonitor:
    def __init__(self, area):
        self.area = area
        self.violated_ids = set()

    def process(self, obj_id: int, cx: int, cy: int) -> bool:
        """
        Returns True if a NEW violation occurred.
        """
        inside = point_inside_area(cx, cy, self.area)

        if inside and obj_id not in self.violated_ids:
            self.violated_ids.add(obj_id)
            return True

        return False
