from source.processing.vehicle import Vehicle
from source.utils.variables import *


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

        if vehicle.x1 > self.point_on_line(2, vehicle.y1)[0]:
            self.first_lane += 1
        elif self.point_on_line(3, vehicle.y1)[0] + 300 > vehicle.x1 > self.point_on_line(3, vehicle.y1)[0] - 300 and \
                self.point_on_line(2, vehicle.y2)[0] + 300 > vehicle.x2 > self.point_on_line(2, vehicle.y2)[0] - 300:
            self.second_lane += 1
        elif self.point_on_line(4, vehicle.y1)[0] + 200 > vehicle.x1 > self.point_on_line(4, vehicle.y1)[0] - 900 and \
                self.point_on_line(3, vehicle.y2)[0] + 300 > vehicle.x2 > self.point_on_line(3, vehicle.y2)[0] - 300:
            self.third_lane += 1
        elif self.point_on_line(5, vehicle.y1)[0] > vehicle.x1 and \
                self.point_on_line(4, vehicle.y2)[0] + 200 > vehicle.x2 > self.point_on_line(4, vehicle.y2)[0] - 200:
            self.fourth_lane += 1
        elif self.point_on_line(6, vehicle.y1)[0] > vehicle.x1:
            self.fifth_lane += 1

    @staticmethod
    def point_on_line(line, y):
        match line:
            case 1:
                x1, y1 = LINE1_PT1
                x2, y2 = LINE1_PT2
            case 2:
                x1, y1 = LINE2_PT1
                x2, y2 = LINE2_PT2
            case 3:
                x1, y1 = LINE3_PT1
                x2, y2 = LINE3_PT2
            case 4:
                x1, y1 = LINE4_PT1
                x2, y2 = LINE4_PT2
            case 5:
                x1, y1 = LINE5_PT1
                x2, y2 = LINE5_PT2
            case 6:
                x1, y1 = LINE6_PT1
                x2, y2 = LINE6_PT2
            case _:
                raise ValueError("line must be in [1, 6]")

        m = (y2 - y1) / (x2 - x1)
        x = (y - y1) / m + x1
        return int(x), int(y)

    def reset(self):
        self.vehicles = 0
        self.cars = 0
        self.trucks = 0
        self.busses = 0
        self.vans = 0
        self.first_lane = 0
        self.second_lane = 0
        self.third_lane = 0
        self.fourth_lane = 0
        self.fifth_lane = 0
