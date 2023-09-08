from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord

class Game:
    board: Board

    def get_board_cells_coord(self) -> [(Cell, CubeCoord)]:
        return [(self.board.get_cell_by_coord(coord), coord) for coord in self.board.coords]
