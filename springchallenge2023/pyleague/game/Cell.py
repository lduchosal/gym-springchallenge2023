from typing import Optional

from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.Player import Player


class Cell:
    NO_CELL = None  # To be defined later
    coord: CubeCoord
    anthill: Optional[Player]

    def __init__(self, index, coord):
        self.index = index
        self.richness = 0
        self.ants = [0, 0]
        self.beacons = [0, 0]
        self.coord = coord
        self.type = CellType.EMPTY
        self.anthill = None

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

    def place_ants(self, player: Player, amount: int):
        self.place_ants_by_idx(player.get_index(), amount)

    def place_ants_by_idx(self, player_idx, amount):
        self.ants[player_idx] += amount

    def remove_ants(self, player, amount):
        self.remove_ants_by_idx(player.get_index(), amount)

    def get_ants(self, player):
        return self.get_ants_by_idx(player.get_index())

    def get_ants_by_idx(self, player_idx):
        return self.ants[player_idx]

    def set_beacon_power(self, player_idx, power):
        self.beacons[player_idx] = power

    def get_beacon_power(self, player_idx):
        return self.beacons[player_idx]

    def get_beacon_power_by_player(self, player):
        return self.beacons[player.get_index()]

    def remove_ants_by_idx(self, player_idx, amount):
        self.ants[player_idx] -= min(amount, self.ants[player_idx])

    def deplete(self, amount):
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
