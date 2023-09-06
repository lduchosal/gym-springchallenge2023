import matplotlib.pyplot as plt
import numpy as np

def plot_hexagon(ax, x_center, y_center):
    """Plots a hexagon centered at (x_center, y_center)"""
    for angle in np.linspace(0, 2*np.pi, 7):
        x = x_center + 1 * np.cos(angle)
        y = y_center + 1 * np.sin(angle)
        ax.plot([x, x_center], [y, y_center], color='black')

fig, ax = plt.subplots()

# Center hexagon
plot_hexagon(ax, 0, 0)

# Surrounding hexagons
angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
for angle in angles:
    x = 2 * np.cos(angle)
    y = 2 * np.sin(angle)
    plot_hexagon(ax, x, y)

ax.axis('equal')
plt.show()
