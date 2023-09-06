import matplotlib.pyplot as plt
import numpy as np

def draw_hexagon(ax, x, y):
    angles = np.linspace(0, 2*np.pi, 7)
    x_hexagon = x + np.cos(angles)
    y_hexagon = y + np.sin(angles)
    ax.plot(x_hexagon, y_hexagon, 'b-')

def cube_to_axial(x, y, z):
    q = x
    r = z
    return q, r

def axial_to_pixel(q, r, size):
    x = size * (3. / 2) * q
    y = size * (np.sqrt(3) / 2 * q  +  np.sqrt(3) * r)
    return x, y

fig, ax = plt.subplots()

size = 1

# Central hexagon in cube coordinates is (0,0,0)
center_q, center_r = cube_to_axial(0, 0, 0)
center_x, center_y = axial_to_pixel(center_q, center_r, size)
draw_hexagon(ax, center_x, center_y)

# Define neighbors in cube coordinates
neighbors_cube = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]

for x, y, z in neighbors_cube:
    q, r = cube_to_axial(x, y, z)
    x, y = axial_to_pixel(q, r, size)
    draw_hexagon(ax, x, y)

ax.axis('equal')
plt.show()
