import matplotlib.pyplot as plt
import numpy as np

def draw_hexagon(ax, x, y):
    angles = np.linspace(0, 2*np.pi, 7)
    x_hexagon = x + np.cos(angles)
    y_hexagon = y + np.sin(angles)
    ax.plot(x_hexagon, y_hexagon, 'b-')

fig, ax = plt.subplots()

# Initial hexagon at origin
draw_hexagon(ax, 0, 0)

# Tiling hexagons
draw_hexagon(ax, 1.5, 0)
draw_hexagon(ax, 0.75, 1.3)
draw_hexagon(ax, -0.75, 1.3)
draw_hexagon(ax, -1.5, 0)

ax.axis('equal')
plt.show()
