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
    length = 100
    width = 100
    diffusion_rate = 0.3
    dispensers = []
    simulation_time = 10
    frame = 0
    stable_density = 0

    def __init__(self, length, width):
        self.y_max = []
        self.y_average = []
        self.y_min = []
        self.x_data = []
        self.average_dens = None
        self.min_dens = None
        self.max_dens = None
        self.time_text = None
        self.im = None
        self.length = length
        self.width = width
        self.grid = np.zeros((width, length))
        self.log_file_name = 'logs/grid_' + time.strftime('%H_%M_%S', time.localtime()) + '.csv'

    def add_dispenser(self, disp):
        self.dispensers.append(disp)

    def set_field_settings(self, simulation_time, diffusion_rate, stable_density):
        self.simulation_time = simulation_time
        self.diffusion_rate = diffusion_rate
        self.stable_density = stable_density
    ##В нужн диапазоне в каком то процент простр (70-80%)
    ##Что-то оптимизировать (пороги, отклонения)
    ##Результаты эксперимента
    def show_field(self):
        fig, (ax, ax_stat) = plt.subplots(2, 1, figsize=(8, 6))

        norm = Normalize(vmin=0, vmax=self.stable_density*2)
        self.im = ax.imshow(self.grid, cmap=cm.hot, norm=norm, interpolation='nearest')
        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.hot), ax=ax, label='Концентрация аромата')
        ax.set_title(self.GRID_TITLE)
        ax.set_xlabel(self.X_LABEL)
        ax.set_ylabel(self.Y_LABEL)
        self.time_text = ax.text(-0.1, 1.1, '', transform=ax.transAxes, ha='center', fontsize=12)

        ax_stat.set_xlim(0, self.simulation_time)
        ax_stat.set_ylim(0, self.stable_density*2)
        self.max_dens, = ax_stat.plot([], [], lw=2, label='Максимальная концентрация')
        self.average_dens, = ax_stat.plot([], [], lw=2, label='Средняя концентрация')
        self.min_dens, = ax_stat.plot([], [], lw=2, label='Минимальная концентрация')
        ax_stat.axhline(y=self.stable_density * 1.2, color='r', linestyle='--')
        ax_stat.axhline(y=self.stable_density * 0.8, color='r', linestyle='--')
        ax_stat.legend()
        ax_stat.set_title('Статистика по концентрации')

        animation = FuncAnimation(fig, self.update, self.simulation_time, interval=1, repeat=False)
        plt.tight_layout()
        plt.show()

    def update(self, frame):
        print("Время: {} сек.".format(self.frame))
        self.spray_dispensers()
        self.save_log_grid_data(self.grid)
        remains_grid = self.get_remains_grid()
        new_grid = self.calc_weights(remains_grid)
        new_grid[new_grid < 0] = 0
        self.grid = new_grid
        self.im.set_array(self.grid)
        self.time_text.set_text("Время: {} сек.".format(self.frame))

        self.x_data.append(self.frame)
        self.y_min.append(np.min(self.grid))
        self.y_average.append(np.mean(self.grid))
        self.y_max.append(np.max(self.grid))
        self.max_dens.set_data(self.x_data, self.y_max)
        self.average_dens.set_data(self.x_data, self.y_average)
        self.min_dens.set_data(self.x_data, self.y_min)

        self.frame += 1
        return self.im, self.time_text, self.max_dens, self.average_dens, self.min_dens

    def simulate(self):
        time_start = time.time()
        print("Начало: {}".format(time_start))
        for i in range(0, self.simulation_time):
            self.frame = i
            self.spray_dispensers()
            self.save_log_grid_data(self.grid)
            # remains_grid = self.get_remains_grid_bad_version()
            remains_grid = self.get_remains_grid()
            new_grid = self.calc_weights(remains_grid)
            new_grid[new_grid < 0] = 0
            self.grid = new_grid
            self.x_data.append(self.frame)
            self.y_min.append(np.min(self.grid))
            self.y_average.append(np.mean(self.grid))
            self.y_max.append(np.max(self.grid))
        time_end = time.time()
        print("Конец: {}".format(time_end))
        print("Время выполнения: {}".format(time_end-time_start))

    def spray_dispensers(self):
        for disp in self.dispensers:
            x_start, x_end = disp.get_x_row(self.grid)
            y_start, y_end = disp.get_y_row(self.grid)
            x_range = slice(x_start, x_end) if x_start != x_end else slice(x_start, x_start+1)
            y_range = slice(y_start, y_end) if y_start != y_end else slice(y_start, y_start+1)
            spray_grid = disp.spray(self.frame, self.grid)
            self.grid[x_range, y_range] += spray_grid

    def save_log_grid_data(self, grid):
        with open(self.log_file_name, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow('Итерация: ' + str(self.frame))
            writer.writerows(grid)
            writer.writerow(np.full(100, '-'))

    def get_remains_grid(self):
        return self.grid * (1-self.diffusion_rate)

    def get_remains_grid_bad_version(self):
        remain_grid = np.zeros((self.width, self.length))
        rate = 1-self.diffusion_rate
        for i in range(0, self.width):
            for j in range(0, self.length):
                remain_grid[i, j] = self.grid[i, j] * rate
        return remain_grid

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
        if i == 0 or i == self.width - 1:
            divider -= 1
        if j == 0 or j == self.length - 1:
            divider -= 1
        return divider
