from typing import Optional

from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.Player import Player


class Cell:
    NO_CELL = None  # To be defined later

    def __init__(self, index, coord: CubeCoord):
        self.index: int = index
        self.richness: int = 0
        self.ants: [int] = [0, 0]
        self.beacons: [int] = [0, 0]
        self.coord: CubeCoord = coord
        self.type: CellType = CellType.EMPTY
        self.anthill: Optional[Player] = None

    def __str__(self):
        return f'[{self.index}] {self.type} {self.richness} ({self.coord.x}, {self.coord.y}, {self.coord.z})'

    def get_index(self):
        return self.index

    def is_valid(self):
        return True

    def set_food_amount(self, richness):
        self.richness = richness
        self.type = CellType.FOOD

    def get_richness(self):
        return self.richness

    def get_spawn_power(self):
        return self.richness

    def set_spawn_power(self, richness):
        self.richness = richness
        self.type = CellType.EGG

    def get_anthill(self):
        return self.anthill

    def get_coord(self):
        return self.coord

    def set_anthill(self, anthill):
        self.anthill = anthill

    def place_ants_by_player(self, player: Player, amount: int):
        self.place_ants_by_idx(player.index, amount)

    def place_ants_by_idx(self, player_idx, amount):
        self.ants[player_idx] += amount

    def remove_ants_by_player(self, player: Player, amount: int):
        self.remove_ants_by_idx(player.index, amount)

    def remove_ants_by_idx(self, player_idx: int, amount: int):
        self.ants[player_idx] -= min(amount, self.ants[player_idx])

    def get_ants_by_player(self, player: Player):
        return self.get_ants_by_idx(player.index)

    def get_ants_by_idx(self, player_idx: int) -> int:
        return self.ants[player_idx]

    def set_beacon_power(self, player_idx: int, power: int):
        self.beacons[player_idx] = power

    def get_beacon_power_by_idx(self, player_idx: int):
        return self.beacons[player_idx]

    def get_beacon_power_by_player(self, player: Player):
        return self.get_beacon_power_by_idx(player.index)

    def deplete(self, amount: int):
        self.richness -= min(amount, self.richness)

    def get_type(self):
        return self.type

    def remove_beacons(self):
        self.beacons = [0, 0]

    def get_all_ants(self):
        return self.ants


class NoCell(Cell):
    def __init__(self):
        super().__init__(-1, None)

    def is_valid(self):
        return False

    def get_index(self):
        return -1


Cell.NO_CELL = NoCell()
