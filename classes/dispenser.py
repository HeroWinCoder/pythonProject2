class Dispenser:
    x = 0
    y = 0
    interval = 5
    portion_per_dispense = 2

    def __init__(self, x, y, interval, portion_per_dispense):
        self.x = x
        self.y = y
        self.interval = interval
        self.portion_per_dispense = portion_per_dispense


    def spray(self):
        return self.portion_per_dispense