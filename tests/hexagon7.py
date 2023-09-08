import matplotlib.pyplot as plt
import numpy as np

def draw_hexagon(ax, x, y, color='blue', label=None):
    angles = np.linspace(np.pi/6, 2*np.pi + np.pi/6, 7)
    x_hexagon = x + np.cos(angles)
    y_hexagon = y + np.sin(angles)
    ax.plot(x_hexagon, y_hexagon, 'b-')
    # ax.fill(x_hexagon, y_hexagon, color)
    if label is not None:
        ax.text(x, y, label, fontsize=12, ha='center', va='center')

def cube_to_axial(x, y, z):
    q = x
    r = z
    return q, r

def axial_to_pixel_pointy(q, r, size):
    x = size * (np.sqrt(3) * q  +  np.sqrt(3)/2 * r)
    y = size * (3./2 * r)
    return x, y

fig, ax = plt.subplots()

size = 1

# Central hexagon in cube coordinates is (0,0,0)
center_q, center_r = cube_to_axial(0, 0, 0)
center_x, center_y = axial_to_pixel_pointy(center_q, center_r, size)
draw_hexagon(ax, center_x, center_y, color='red', label='0')

# Define neighbors in cube coordinates
neighbors_cube = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]

neighbors_cube = [
    (0, 0, 0),
    (1, -1, 0),
    (-1, 1, 0),
    (2, -2, 0),
    (-2, 2, 0),
]

for x, y, z in neighbors_cube:
    q, r = cube_to_axial(x, y, z)
    x, y = axial_to_pixel_pointy(q, r, size)
    draw_hexagon(ax, x, y)

ax.axis('equal')
plt.show()
