from vision.geometry import point_inside_area


class AreaCounter:
    def __init__(self, area, area_top_y, area_bottom_y):
        self.area = area
        self.area_top_y = area_top_y
        self.area_bottom_y = area_bottom_y

        self.last_inside_state = {}
        self.entry_side = {}
        self.counted_objects = set()

        self.up_count = 0
        self.down_count = 0

    def process(self, obj_id: int, cx: int, cy: int):
        inside = point_inside_area(cx, cy, self.area)

        # First appearance
        if obj_id not in self.last_inside_state:
            self.last_inside_state[obj_id] = inside
            return

        prev_inside = self.last_inside_state[obj_id]

        # Outside → Inside
        if not prev_inside and inside:
            if cy < self.area_top_y:
                self.entry_side[obj_id] = "top"
            elif cy > self.area_bottom_y:
                self.entry_side[obj_id] = "bottom"

        # Inside → Outside
        elif prev_inside and not inside:
            if obj_id in self.counted_objects:
                self.last_inside_state[obj_id] = inside
                return

            if obj_id in self.entry_side:
                if self.entry_side[obj_id] == "top":
                    self.down_count += 1
                elif self.entry_side[obj_id] == "bottom":
                    self.up_count += 1

                self.counted_objects.add(obj_id)
                del self.entry_side[obj_id]

        self.last_inside_state[obj_id] = inside
