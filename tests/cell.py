import matplotlib.pyplot as plt
import numpy as np


def draw_pointy_hexagon(center_x, center_y, size):
    angles = np.linspace(0, 2 * np.pi, 7)
    x = center_x + size * np.sin(angles)
    y = center_y + size * np.cos(angles)
    plt.plot(x, y, 'b-')


plt.figure()
draw_pointy_hexagon(0, 0, 1)
plt.axis('equal')
plt.show()