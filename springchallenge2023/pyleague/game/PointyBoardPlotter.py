import numpy as np

from springchallenge2023.pyleague.game import Board
from springchallenge2023.pyleague.game import Cell
from springchallenge2023.pyleague.game import CellType
from springchallenge2023.pyleague.game import CubeCoord


class PointyBoardPlotter:
    def draw_hexagon(self, ax, x: int, y: int, text: str, bgcolor: str = 'white', textcolor: str = 'black'):

        angles = np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)
        x_hexagon = x + np.cos(angles)
        y_hexagon = y + np.sin(angles)
        ax.plot(x_hexagon, y_hexagon, 'b-')
        ax.fill(x_hexagon, y_hexagon, bgcolor)
        ax.text(x, y, text, fontsize=10, ha='center', va='center', color=textcolor)

    def draw_cell(self, ax, cell: Cell):
        coord = cell.coord
        q, r = self.cube_to_axial(coord.x, coord.y, coord.z)
        x, y = self.axial_to_pixel(q, r)
        text = str(cell.index)
        text = f'{cell.index}\n{coord.x},{coord.y},{coord.z}'
        text = f'{cell.index}'

        textcolor = 'grey'
        bgcolor = 'white'
        if cell.anthill is not None:
            bgcolor = "red" if cell.anthill.index == 1 else "blue"
            textcolor = 'white'
            ressources = str(cell.ants[cell.anthill.index])
            richness = str(cell.richness)
            text = f'{text}\n{ressources}\n{richness}'

        if cell.richness > 0:
            richness = str(cell.richness)
            text = f'{text}\n{richness}'
            bgcolor = "yellow" if cell.type == CellType.FOOD else "green"
            textcolor = 'black' if cell.type == CellType.FOOD else "white"

        self.draw_hexagon(ax, x, y, text, bgcolor, textcolor)

    def cube_to_axial(self, x, y, z):
        q = x
        r = z
        return q, r

    def axial_to_pixel(self, q, r, size: int = 1.0):
        x = size * (np.sqrt(3) * q + np.sqrt(3) / 2 * r)
        y = size * (3. / 2 * r)
        return x, y

    def hexagon_grid(self, ax, neighbors_cube: [(int,int,int)]):

        i = 0
        for x, y, z in neighbors_cube:
            q, r = self.cube_to_axial(x, y, z)
            x, y = self.axial_to_pixel(q, r)
            self.draw_hexagon(ax, x, y, f'{i}')
            i += 1

        ax.axis('equal')
        return ax


    def plot_board(self, ax, board: Board):

        for cell in board.cells:
            self.draw_cell(ax, cell)

        ax.axis('equal')
        return ax

    def plot_grid(self, ax, grid: [CubeCoord]):

        index = 0
        for coord in grid:
            cell = Cell(index, coord)
            self.draw_cell(ax, cell)
            index += 1

        ax.axis('equal')
        return ax

