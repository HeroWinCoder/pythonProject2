import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from matplotlib.colors import Normalize


def ask_user_for_parameters():
    length = float(input("Введите длину комнаты в метрах: "))
    width = float(input("Введите ширину комнаты в метрах: "))
    height = float(input("Введите высоту потолков в метрах: "))
    diffusion_rate = float(input("Введите коэффициент диффузии: "))
    simulation_time = int(input("Введите общее время моделирования в секундах: "))
    spray_interval = int(input("Введите интервал распыления в секундах: "))
    spray_volume_per_interval = float(input("Введите объем духов, распыляемый за один раз в миллилитрах: "))
    grid_size = int(input("Введите размер сетки для симуляции: "))
    num_spray_points = int(input("Введите количество точек распыления: "))
    spray_points = []
    for i in range(num_spray_points):
        x = int(input(f"Введите координату X точки распыления {i + 1} (от 0 до {grid_size - 1}): "))
        y = int(input(f"Введите координату Y точки распыления {i + 1} (от 0 до {grid_size - 1}): "))
        spray_points.append((x, y))

    return (grid_size, diffusion_rate, simulation_time, spray_interval,
            spray_volume_per_interval, length, width, height, spray_points)


(grid_size, diffusion_rate, simulation_time, spray_interval,
 spray_volume_per_interval, length, width, height, spray_points) = ask_user_for_parameters()

grid = np.zeros((grid_size, grid_size))


def update(frame_num):
    global grid
    new_grid = np.copy(grid)

    # Распыляем духи в указанные интервалы
    if frame_num % spray_interval == 0:
        for x, y in spray_points:
            new_grid[x, y] += spray_volume_per_interval

    # Диффузия
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            diffusion = (grid[i - 1, j] + grid[i + 1, j] +
                         grid[i, j - 1] + grid[i, j + 1] -
                         4 * grid[i, j]) * diffusion_rate
            new_grid[i, j] += diffusion

    new_grid[new_grid < 0] = 0
    grid = new_grid

    im.set_array(grid)
    return im,


fig, ax = plt.subplots(figsize=(8, 8))
norm = Normalize(vmin=0, vmax=spray_volume_per_interval)
im = ax.imshow(grid, cmap=cm.hot, norm=norm, interpolation='nearest')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.hot), ax=ax, label='Концентрация аромата')
ax.set_title("Распределение аромата в комнате")
plt.xlabel("Вид сверху на комнату, ось X")
plt.ylabel("Вид сверху на комнату, ось Y")
plt.text(0, -grid_size // 10,
         "Каждый 'шаг' анимации представляет один этап времени, в течение которого духи диффундируют.\n"
         "Карта цветов показывает концентрацию аромата: от низкой (тёмные тона) до высокой (светлые тона).",
         ha='left', wrap=True)

ani = FuncAnimation(fig, update, frames=simulation_time, interval=1000, repeat=False)

plt.show()
