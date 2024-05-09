import classes.field as field
import classes.dispenser as dispenser

field = field.Field(100, 100, 2)
field.add_dispenser(dispenser.Dispenser(3, 3, 1, 100, [10, 1]))
field.add_dispenser(dispenser.Dispenser(50, 40, 1, 100, [10, 1]))
field.add_dispenser(dispenser.Dispenser(90, 90, 1, 50, [1, 10]))
field.set_field_settings(1000, 0.8)
field.show_field()
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# num_points = 100
# x = np.random.randint(0, 10, num_points)
# y = np.random.randint(0, 10, num_points)
# z = np.random.randint(0, 10, num_points)
# weights = np.random.rand(num_points) * 5
#
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# cmap = plt.get_cmap('cool')
# sc = ax.scatter(x, y, z, c=weights, cmap=cmap)
# plt.colorbar(sc, label='Weights')
#
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Bar Plot with Weighted Colors')
#
# plt.show()