import matplotlib.pyplot as plt
import numpy as np

def draw_hexagon(ax, x, y, text):
    angles = np.linspace(0, 2*np.pi, 7)
    x_hexagon = x + np.cos(angles)
    y_hexagon = y + np.sin(angles)
    ax.plot(x_hexagon, y_hexagon, 'b-')
    ax.text(x, y, text, fontsize=12, ha='center', va='center')

def cube_to_axial(x, y, z):
    q = x
    r = z
    return q, r

def axial_to_pixel(q, r, size):
    x = size * (3. / 2) * q
    y = size * (np.sqrt(3) / 2 * q  +  np.sqrt(3) * r)
    return x, y

def axial_to_pixel_pointy(q, r, size):
    x = size * (np.sqrt(3) * q  +  np.sqrt(3)/2 * r)
    y = size * (3./2 * r)
    return x, y

fig, ax = plt.subplots()

size = 1

# Define neighbors in cube coordinates
neighbors_cube = [
        (0, 0, 0),

        (1, 0, -1), (-1, 0, 1),
        (1, -1, 0), (-1, 1, 0),
        (0, -1, 1), (0, 1, -1),

        (2, 0, -1), (-2, 0, 1),
        (2, -1, 0), (-2, 1, 0),
        (1, -1, 1), (-1, 1, -1),

]

neighbors_cube = [
    (0, 0, 0),
    (1, -1, 0),
    (-1, 1, 0),
    (2, -2, 0),
    (-2, 2, 0),
]

i = 0
for x, y, z in neighbors_cube:
    q, r = cube_to_axial(x, y, z)
    x, y = axial_to_pixel(q, r, size)
    draw_hexagon(ax, x, y, f'{i}')
    i += 1

ax.axis('equal')
plt.show()
