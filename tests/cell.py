import matplotlib.pyplot as plt
import numpy as np


def draw_pointy_hexagon(ax: plt, center_x: int, center_y: int, size: int):
    angles = np.linspace(0, 2 * np.pi, 7)
    x = center_x + size * np.sin(angles)
    y = center_y + size * np.cos(angles)
    ax.plot(x, y, 'b-')


def draw_rhombus(ax: plt, center_x: int, center_y: float, width: float, height: float):
    x = np.array([center_x, center_x + width / 2, center_x, center_x - width / 2, center_x])
    y = np.array([center_y - height / 2, center_y, center_y + height / 2, center_y, center_y - height / 2])
    ax.plot(x, y, 'r-')


def draw_cell(ax: plt, center_x: int, center_y: int, size: int):
    draw_pointy_hexagon(ax, center_x, center_y, size)
    draw_rhombus(ax, center_x, center_y + size * -0.6, size * 1.2, size * 0.7)
    draw_rhombus(ax, center_x, center_y + size * 0.6, size * 1.2, size * 0.7)

plt.figure(figsize=(1024/100, 768/100), dpi=200)

size = 5
draw_cell(plt, 0, 0, size)
draw_cell(plt, size*2, 0, size)
draw_cell(plt, 0, size*2, size)
draw_cell(plt, size*2, size*2, size)

plt.axis('equal')
plt.show()
