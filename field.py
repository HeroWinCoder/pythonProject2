import classes.dispenser as dispenser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.colors import Normalize
from matplotlib import cm
import csv
import time


class Field:
    GRID_TITLE = 'Распределение аромата в комнате'
    X_LABEL = 'ось X'
    Y_LABEL = 'ось Y'
    Z_LABEL = 'ось Z'
    DESCRIPTION_TEXT = "Каждый 'шаг' анимации представляет один этап времени, в течение которого духи диффуззируют.\n " \
                       "Карта цветов показывает концентрацию аромата: от низкой (тёмные тона) до высокой (светлые тона).\n\n"
    length = 100
    width = 100
    height = 2
    diffusion_rate = 0.3
    dispensers = []
    simulation_time = 10
    frame = 0
    stable_density = 0

    def __init__(self, length, width, height):
        self.ax = None
        self.scatter = None
        self.length = length
        self.width = width
        self.height = height
        self.grid = np.zeros((width, length, height))
        self.log_file_name = 'logs/grid_' + time.strftime('%H_%M_%S', time.localtime()) + '.csv'

    def add_dispenser(self, disp):
        self.dispensers.append(disp)

    def set_field_settings(self, simulation_time, diffusion_rate, stable_density, interval):
        self.simulation_time = simulation_time
        self.diffusion_rate = diffusion_rate
        self.stable_density = stable_density
        self.interval = interval

    def show_field(self):
        frames = []
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        norm = Normalize(vmin=0, vmax=self.stable_density*2)
        indices = np.where(self.grid > 0)
        x, y, z = indices[0], indices[1], indices[2]
        weights = self.grid[indices]
        frames.append([self.ax.scatter(x, y, z, c=weights, cmap=cm.hot, norm=norm)])
        for f in range(self.simulation_time):
            frames.append([self.update()])
        # self.scatter = ax.scatter(x, y, z, c=weights, cmap=cm.hot, norm=norm)
        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.hot), ax=self.ax, label='Концентрация аромата')
        self.ax.set_title(self.GRID_TITLE)
        self.ax.set_xlabel(self.X_LABEL)
        self.ax.set_ylabel(self.Y_LABEL)
        self.ax.set_zlabel(self.Z_LABEL)
        animation = ArtistAnimation(fig, frames, interval=self.interval, repeat=False)
        plt.show()

    def get_max_portion_from_dispensers(self):
        max_portion = 0
        for disp in self.dispensers:
            max_portion = max(max_portion, disp.portion_per_dispense)
        return max_portion

    def update(self):
        print("Время: {} сек.".format(self.frame))
        self.spray_dispensers()
        self.save_log_grid_data(self.grid)
        remains_grid = self.get_remains_grid()
        new_grid = self.calc_weights(remains_grid)
        new_grid[new_grid < 0] = 0
        self.grid = new_grid
        new_indices = np.where(new_grid > 0)
        x, y, z = new_indices[0], new_indices[1], new_indices[2]
        weights = new_grid[new_indices]
        self.frame += 1
        return self.ax.scatter(x, y, z, c=weights, cmap=cm.hot)

    def spray_dispensers(self):
        for disp in self.dispensers:
            x_start, x_end = disp.get_x_row(self.grid)
            y_start, y_end = disp.get_y_row(self.grid)
            z_start, z_end = disp.get_z_row(self.grid)
            x_range = slice(x_start, x_end) if x_start != x_end else slice(x_start, x_start + 1)
            y_range = slice(y_start, y_end) if y_start != y_end else slice(y_start, y_start + 1)
            z_range = slice(z_start, z_end) if z_start != z_end else slice(z_start, z_start + 1)
            spray_grid = disp.spray(self.frame, self.grid)
            self.grid[x_range, y_range, z_range] += spray_grid

    def save_log_grid_data(self, grid):
        with open(self.log_file_name, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow('Итерация: ' + str(self.frame))
            writer.writerows(grid)
            writer.writerow(np.full(100, '-'))

    def get_remains_grid(self):
        return self.grid * (1 - self.diffusion_rate)

    def calc_weights(self, ratio_grid):
        new_grid = np.zeros((self.width, self.length, self.height))
        for i in range(0, self.width):
            for j in range(0, self.length):
                for k in range(0, self.height):
                    new_grid[i, j, k] = ratio_grid[i, j, k] + self.get_neighbors_profit(i, j, k)
        return new_grid

    def get_neighbors_profit(self, i, j, k):
        neighbors_profit = 0
        if i - 1 >= 0:
            neighbors_profit += self.grid[i - 1, j, k] * self.diffusion_rate / self.get_neighbor_divider(i - 1, j, k)
        if i + 1 < self.width:
            neighbors_profit += self.grid[i + 1, j, k] * self.diffusion_rate / self.get_neighbor_divider(i + 1, j, k)
        if j - 1 >= 0:
            neighbors_profit += self.grid[i, j - 1, k] * self.diffusion_rate / self.get_neighbor_divider(i, j - 1, k)
        if j + 1 < self.length:
            neighbors_profit += self.grid[i, j + 1, k] * self.diffusion_rate / self.get_neighbor_divider(i, j + 1, k)
        if k - 1 >= 0:
            neighbors_profit += self.grid[i, j, k - 1] * self.diffusion_rate / self.get_neighbor_divider(i, j, k - 1)
        if k + 1 < self.height:
            neighbors_profit += self.grid[i, j, k + 1] * self.diffusion_rate / self.get_neighbor_divider(i, j, k + 1)
        return neighbors_profit

    def get_neighbor_divider(self, i, j, k):
        divider = 6
        if i == 0 or i == self.width:
            divider -= 1
        if j == 0 or j == self.length:
            divider -= 1
        if k == 0 or k == self.length:
            divider -= 1
        return divider
