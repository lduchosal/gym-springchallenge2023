import numpy as np
from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord


class CoordConverter:
    def cube_to_axial(self, x, y, z):
        q = x
        r = z
        return q, r

    def axial_to_pixel(self, q, r, size: int = 1.0):
        x = size * (np.sqrt(3) * q + np.sqrt(3) / 2 * r)
        y = size * (3. / 2 * r)
        return x, y


class HexPlotter:

    def __init__(self):
        self.coord_converter = CoordConverter()

    def draw_rhombus(self, ax: plt, center_x: int, center_y: float, width: float, height: float, bgcolor: str, text: str):
        x = np.array([center_x, center_x + width / 2, center_x, center_x - width / 2, center_x])
        y = np.array([center_y - height / 2, center_y, center_y + height / 2, center_y, center_y - height / 2])
        ax.plot(x, y, 'w-')
        ax.fill(x, y, bgcolor)
        ax.text(center_x, center_y, text, fontsize=10, ha='center', va='center', color='white')


    def draw_hexagon(self, ax, x: int, y: int, size: float, text: str, bgcolor: str = 'white', textcolor: str = 'black'):

        angles = np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)
        x_hexagon = x + size * np.cos(angles)
        y_hexagon = y + size * np.sin(angles)
        ax.plot(x_hexagon, y_hexagon, 'b-')
        ax.fill(x_hexagon, y_hexagon, bgcolor)
        ax.text(x, y, text, fontsize=10, ha='center', va='center', color=textcolor)

    def draw_cell(self, ax, cell: Cell):
        coord = cell.coord
        q, r = self.coord_converter.cube_to_axial(coord.x, coord.y, coord.z)
        x, y = self.coord_converter.axial_to_pixel(q, r)
        text = str(cell.index)
        text = f'{cell.index}\n{coord.x},{coord.y},{coord.z}'
        text = f'{cell.index}'

        textcolor = 'grey'
        bgcolor = 'white'
        if cell.anthill is not None:
            bgcolor = "red" if cell.anthill.index == 1 else "blue"
            textcolor = 'white'
            text = f'{text}'

        if cell.richness > 0:
            richness = str(cell.richness)
            text = f'{richness}'
            bgcolor = "yellow" if cell.type == CellType.FOOD else "green"
            textcolor = 'black' if cell.type == CellType.FOOD else "white"
        size = 1.0

        self.draw_hexagon(ax, x, y, size, text, bgcolor, textcolor)
        if cell.ants[1] > 0:
            self.draw_rhombus(ax, x, size * -0.6, size * 1.2, size * 0.7, 'red', str(cell.ants[1]))

        if cell.ants[0] > 0:
            self.draw_rhombus(ax, x, size * 0.6, size * 1.2, size * 0.7, 'blue', str(cell.ants[0]))


class PointyBoardPlotter:

    def __init__(self):
        self.hexplotter = HexPlotter()


    def hexagon_grid(self, ax, neighbors_cube: [(int,int,int)]):

        i = 0
        for x, y, z in neighbors_cube:
            q, r = self.cube_to_axial(x, y, z)
            x, y = self.axial_to_pixel(q, r)
            self.hexplotter.draw_hexagon(ax, x, y, f'{i}')
            i += 1

        ax.axis('equal')
        return ax


    def plot_board(self, ax, board: Board):

        for cell in board.cells:
            self.hexplotter.draw_cell(ax, cell)

        ax.axis('equal')
        return ax

    def plot_grid(self, ax, grid: [CubeCoord]):

        index = 0
        for coord in grid:
            cell = Cell(index, coord)
            self.hexplotter.draw_cell(ax, cell)
            index += 1

        ax.axis('equal')
        return ax

