import javarandom
from javarandom import Random

from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.BoardGenerator import BoardGenerator
from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.Player import Player


class Game:

    random: Random = None
    board: Board
    players: [Player]
    gameTurn: int


    def __init__(self, seed: int):
        self.players = [Player(0), Player(1)]
        self.random = javarandom.Random(seed)
        self.gameTurn = 0
        self.board = BoardGenerator.generate(self.random, self.players)


    def get_board_cells_coord(self) -> [(Cell, CubeCoord)]:
        return [(self.board.get_cell_by_coord(coord), coord) for coord in self.board.coords]


    def getGlobalInfoFor(self, player):
        lines = []
        lines.append(str(len(self.board.coords)))
        for coord in self.board.coords:
            cell = self.board.map[coord]
            cell_type = 1 if cell.get_type() == 'EGG' else 2 if cell.get_type() == 'FOOD' else 0
            lines.append(f"{cell_type} {cell.get_richness()} {self.board.get_neighbour_ids(coord)}")

        other = self.getOpponent(player)
        lines.append(str(len(player.anthills)))
        lines.append(" ".join(map(str, player.anthills)))
        lines.append(" ".join(map(str, other.anthills)))

        return lines

    def getOpponent(self, player: Player):
        return self.players[1 - player.get_index()]
