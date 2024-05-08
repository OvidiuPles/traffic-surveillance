class Vehicle:
    def __init__(self, x1, y1, x2, y2, id, frame_depth=0, is_counted=False, number_plate=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.id = id
        self.frame_depth = frame_depth
        self.is_counted = is_counted
        self.number_plate = number_plate
