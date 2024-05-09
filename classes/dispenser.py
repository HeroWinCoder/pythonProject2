import numpy as np


class Dispenser:
    position = [0, 0]
    interval = 5
    portion_per_dispense = 2
    feed_rate = [0, 0]

    def __init__(self, x, y, interval, portion_per_dispense, feed_rate):
        self.position = [x, y]
        self.interval = interval
        self.portion_per_dispense = portion_per_dispense
        self.feed_rate = feed_rate

    def spray(self, frame, grid):
        x_row_start, x_row_end = self.get_x_row(grid)
        y_row_start, y_row_end = self.get_y_row(grid)
        if frame % self.interval == 0:
            portion_per_cell = self.portion_per_dispense/((x_row_end-x_row_start)*(y_row_end-y_row_start))
            return np.full([x_row_end-x_row_start, y_row_end-y_row_start], portion_per_cell)
        else:
            return np.full([x_row_end-x_row_start, y_row_end-y_row_start], 0)

    def get_x_row(self, grid):
        spray_range = np.add(self.position, self.feed_rate)
        x_row_start = min(self.position[0], spray_range[0])
        x_row_end = max(self.position[0], spray_range[0])
        x_grid_len = grid.shape[0]
        if spray_range[0] >= x_grid_len:
            x_row_start = self.position[0]
            x_row_end = x_grid_len-1
        if spray_range[0] < 0:
            x_row_start = 0
            x_row_end = self.position[0]
        return x_row_start, x_row_end

    def get_y_row(self, grid):
        spray_range = np.add(self.position, self.feed_rate)
        y_row_start = min(self.position[1], spray_range[1])
        y_row_end = max(self.position[1], spray_range[1])
        y_grid_len = grid.shape[1]
        if spray_range[1] >= y_grid_len:
            y_row_start = self.position[1]
            y_row_end = y_grid_len-1
        if spray_range[1] < 0:
            y_row_start = 0
            y_row_end = self.position[1]
        return y_row_start, y_row_end
