from source.processing.vehicle import Vehicle


class Counter:
    def __init__(self):
        self.vehicles = 0
        self.cars = 0
        self.trucks = 0
        self.busses = 0
        self.vans = 0
        self.first_lane = 0  # right to left
        self.second_lane = 0
        self.third_lane = 0
        self.fourth_lane = 0
        self.fifth_lane = 0

    def count(self, vehicle: Vehicle):
        self.vehicles += 1
        match vehicle.class_id:
            case 0:
                self.cars += 1
            case 1:
                self.trucks += 1
            case 2:
                self.busses += 1
            case 3:
                self.vans += 1

    @staticmethod
    def point_on_line(y):
        x1, y1 = 2500, 0
        x2, y2 = 3950, 2160

        m = (y2 - y1) / (x2 - x1)
        x = (y - y1) / m + x1
        return int(x), int(y)
