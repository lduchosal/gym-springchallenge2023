from typing import List

from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.Player import Player


class AntConsumption:
    def __init__(self, player: Player, amount: int, cell: Cell, path: List[Cell]) -> None:
        self.player = player
        self.amount = amount
        self.cell = cell
        self.path = path
