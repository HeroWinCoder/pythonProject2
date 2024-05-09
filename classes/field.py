import classes.dispenser as dispenser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib import cm
import csv
import time


class Field:
    GRID_TITLE = 'Распределение аромата в комнате'
    X_LABEL = 'Вид сверху на комнату, ось X'
    Y_LABEL = 'Вид сверху на комнату, ось Y'
    DESCRIPTION_TEXT = "Каждый 'шаг' анимации представляет один этап времени, в течение которого духи диффуззируют.\n " \
                       "Карта цветов показывает концентрацию аромата: от низкой (тёмные тона) до высокой (светлые тона).\n\n"
    length = 100
    width = 100
    height = 2
    diffusion_rate = 0.3
    dispensers = []
    simulation_time = 10
    frame = 0

    def __init__(self, length, width, height):
        self.im = None
        self.length = length
        self.width = width
        self.height = height
        self.grid = np.zeros((width, length))
        self.log_file_name = 'logs/grid_' + time.strftime('%H_%M_%S', time.localtime()) + '.csv'

    def add_dispenser(self, disp):
        self.dispensers.append(disp)

    def set_field_settings(self, simulation_time, diffusion_rate):
        self.simulation_time = simulation_time
        self.diffusion_rate = diffusion_rate

    def show_field(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        norm = Normalize(vmin=0, vmax=self.get_max_portion_from_dispensers()*1)
        self.im = ax.imshow(self.grid, cmap=cm.hot, norm=norm, interpolation='nearest')
        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.hot), ax=ax, label='Концентрация аромата')
        ax.set_title(self.GRID_TITLE)
        animation = FuncAnimation(fig, self.update, self.simulation_time, interval=10, repeat=False)
        plt.xlabel(self.X_LABEL)
        plt.ylabel(self.Y_LABEL)
        plt.text(self.length // 10, 0, self.DESCRIPTION_TEXT, ha='left', wrap=True)
        plt.show()

    def get_max_portion_from_dispensers(self):
        max_portion = 0
        for disp in self.dispensers:
            max_portion = max(max_portion, disp.portion_per_dispense)
        return max_portion

    def update(self, frame):
        self.spray_dispensers()
        self.save_log_grid_data(self.grid)
        remains_grid = self.get_remains_grid()
        new_grid = self.calc_weights(remains_grid)
        new_grid[new_grid < 0] = 0
        self.grid = new_grid
        self.im.set_array(self.grid)
        self.frame += 1
        return self.im,

    def spray_dispensers(self):
        for disp in self.dispensers:
            x_start, x_end = disp.get_x_row(self.grid)
            y_start, y_end = disp.get_y_row(self.grid)
            self.grid[x_start:x_end, y_start:y_end] += disp.spray(self.frame, self.grid)

    def save_log_grid_data(self, grid):
        with open(self.log_file_name, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow('Итерация: ' + str(self.frame))
            writer.writerows(grid)
            writer.writerow(np.full(100, '-'))

    def get_remains_grid(self):
        return self.grid * (1-self.diffusion_rate)

    def calc_weights(self, ratio_grid):
        new_grid = np.zeros((self.width, self.length))
        for i in range(0, self.width):
            for j in range(0, self.length):
                new_grid[i, j] = ratio_grid[i, j] + self.get_neighbors_profit(i, j)
        return new_grid

    def get_neighbors_profit(self, i, j):
        neighbors_profit = 0
        if i - 1 >= 0:
            neighbors_profit += self.grid[i - 1, j] * self.diffusion_rate / self.get_neighbor_divider(i - 1, j)
        if i + 1 < self.width:
            neighbors_profit += self.grid[i + 1, j] * self.diffusion_rate / self.get_neighbor_divider(i + 1, j)
        if j - 1 >= 0:
            neighbors_profit += self.grid[i, j - 1] * self.diffusion_rate / self.get_neighbor_divider(i, j - 1)
        if j + 1 < self.length:
            neighbors_profit += self.grid[i, j + 1] * self.diffusion_rate / self.get_neighbor_divider(i, j + 1)
        return neighbors_profit

    def get_neighbor_divider(self, i, j):
        divider = 4
        if i == 0 or i == self.width:
            divider -= 1
        if j == 0 or j == self.length:
            divider -= 1
        return divider
