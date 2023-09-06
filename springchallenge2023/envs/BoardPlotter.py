import matplotlib.pyplot as plt
import numpy as np

def draw_hexagon(ax, x: int, y: int, text: str):
    angles = np.linspace(0, 2*np.pi, 7)
    x_hexagon = x + np.cos(angles)
    y_hexagon = y + np.sin(angles)
    ax.plot(x_hexagon, y_hexagon, 'b-')
    ax.text(x, y, text, fontsize=12, ha='center', va='center')

def cube_to_axial(x: int, y: int, z: int):
    q = x
    r = z
    return q, r

def axial_to_pixel(q: float, r: int, size: int):
    x = size * (3. / 2) * q
    y = size * (np.sqrt(3) / 2 * q  +  np.sqrt(3) * r)
    return x, y

def hexagon_grid(ax, neighbors_cube: [(int,int,int)]):

    size = 1.1
    i = 0
    for x, y, z in neighbors_cube:
        q, r = cube_to_axial(x, y, z)
        x, y = axial_to_pixel(q, r, size)
        draw_hexagon(ax, x, y, f'{i}')
        i += 1

    ax.axis('equal')
    return ax

