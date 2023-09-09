import numpy as np

from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Cell import Cell

class FlatBoardPlotter:

    def draw_hexagon(self, ax, x: int, y: int, text: str, bgcolor: str = 'white', textcolor: str = 'grey'):
        angles = np.linspace(0, 2*np.pi, 7)
        x_hexagon = x + np.cos(angles)
        y_hexagon = y + np.sin(angles)
        ax.plot(x_hexagon, y_hexagon, 'b-')
        ax.fill(x_hexagon, y_hexagon, bgcolor)
        ax.text(x, y, text, fontsize=12, ha='center', va='center', color=textcolor)

    def draw_cell(self, ax, cell: Cell):
        coord = cell.coord
        q, r = self.cube_to_axial(coord.x, coord.y, coord.z)
        x, y = self.axial_to_pixel(q, r)
        text = str(cell.index)

        textcolor = 'lightgrey'
        bgcolor = 'white'
        if cell.anthill is not None:
            bgcolor = "red" if cell.anthill.index == 1 else "blue"
            textcolor = 'white'
            text = str(cell.ants[cell.anthill.index])

        if cell.richness > 0:
            text = str(cell.richness)
            bgcolor = "yellow"
            textcolor = 'black'

        self.draw_hexagon(ax, x, y, text, bgcolor, textcolor)

    def cube_to_axial(self, x: int, y: int, z: int):
        q = x
        r = z
        return q, r

    def axial_to_pixel(self, q: float, r: int, size: int = 1.1):
        x = size * (3. / 2) * q
        y = size * (np.sqrt(3) / 2 * q  +  np.sqrt(3) * r)
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

