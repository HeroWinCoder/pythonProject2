import classes.dispenser as dispenser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib import cm
import csv
import time





class Field:
    length = 100
    width = 100
    height = 2
    diffusion_rate = 0.3
    dispensers = []

    def __init__(self, length, width, height):
        self.ax = None
        self.simulation_time = None
        self.fig = None
        self.time = None
        self.animation = None
        self.im = None
        self.length = length
        self.width = width
        self.height = height
        self.grid = np.zeros((width, length))

    def add_dispenser(self, x, y, interval, portion_per_dispense):
        self.dispensers.append(dispenser.Dispenser(x, y, interval, portion_per_dispense))

    def set_field_settings(self, simulation_time, diffusion_rate):
        self.simulation_time = simulation_time
        self.diffusion_rate = diffusion_rate
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        norm = Normalize(vmin=0, vmax=100)  # norm = Normalize(vmin=0, vmax=self.get_max_portion_from_dispensers())
        self.im = self.ax.imshow(self.grid, cmap=cm.hot, norm=norm, interpolation='nearest')
        self.fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.hot), ax=self.ax, label='Концентрация аромата')
        self.ax.set_title("Распределение аромата в комнате")

    def show_field(self):
        self.time = time.strftime('%H_%M_%S', time.localtime())
        plt.xlabel("Вид сверху на комнату, ось X")
        plt.ylabel("Вид сверху на комнату, ось Y")
        plt.text(self.length // 10, 0,
                 "Каждый 'шаг' анимации представляет один этап времени, в течение которого духи диффуззируют.\n"
                 "Карта цветов показывает концентрацию аромата: от низкой (тёмные тона) до высокой (светлые тона).\n\n",
                 ha='left', wrap=True)
        self.animation = FuncAnimation(self.fig, self.update, frames=self.simulation_time, interval=100, repeat=False)
        plt.show()

    def update(self, frame_num):
        new_grid = np.copy(self.grid)

        for disp in self.dispensers:
            if frame_num % disp.interval == 0:
                new_grid[disp.x, disp.y] += disp.spray()

        for i in range(1, self.width - 1):
            for j in range(1, self.length - 1):
                diffusion = (self.grid[i - 1, j] + self.grid[i + 1, j] +
                             self.grid[i, j - 1] + self.grid[i, j + 1]) / 4 * self.diffusion_rate
                new_grid[i, j] += diffusion

        new_grid[new_grid < 0] = 0
        self.grid = new_grid
        self.save_log_grid_data(new_grid)

        self.im.set_array(self.grid)
        return self.im,

    def get_max_portion_from_dispensers(self):
        max_portion = 0
        for disp in self.dispensers:
            max_portion = max(max_portion, disp.portion_per_dispense)
        return max_portion

    def save_log_grid_data(self, grid):
        file_name = 'logs/grid_' + self.time + '.csv'
        with open(file_name, 'w+') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(grid)
            writer.writerow(np.full(100, '-'))
