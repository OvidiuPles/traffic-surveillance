from source.processing.vehicle import Vehicle


class Counter:
    def __init__(self):
        self.vehicles = 0
        self.cars = 0
        self.trucks = 0
        self.busses = 0
        self.vans = 0

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
