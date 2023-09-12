from collections import defaultdict
from typing import List

from springchallenge2023.pyleague.game import Player


class GameSummaryManager:

    def __init__(self):
        self.lines = []
        self.players_errors = defaultdict(list)
        self.meal_map = defaultdict(list)
        self.meal_map[0] = []
        self.meal_map[1] = []

        self.egg_map = defaultdict(list)
        self.egg_map[0] = []
        self.egg_map[1] = []

    def get_summary(self):
        return self.__str__()

    def clear(self):
        self.lines.clear()
        self.players_errors.clear()
        self.meal_map[0].clear()
        self.meal_map[1].clear()
        self.egg_map[0].clear()
        self.egg_map[1].clear()

    def __str__(self):
        return self.format_errors() + self.format_lines()

    def add_error(self, player: Player, error: str):
        key = player.index
        self.players_errors[key].append(error)

    def format_lines(self):
        harvest_lines = []
        # (Same logic as in your Java code here, for brevity skipped)
        return "\n".join(harvest_lines + self.lines)

    def format_errors(self):
        if not self.players_errors:
            return ""
        return "\n\n".join([
            f"{key}: {errors[0]} {'+' + str(len(errors) - 1) + ' other error' + ('s' if len(errors) > 2 else '') if len(errors) > 1 else ''}"
            for key, errors in self.players_errors.items()
        ]) + "\n\n"

    def add_not_enough_food_left(self, player):
        self.lines.append(f"{player.index} has harvested at least half the crystals. Game over!")

    def add_no_more_food(self):
        self.lines.append("All the crystals have been harvested. Game over!")

    def add_build(self, meal):
        self.egg_map[meal.player.index].append(meal)

    def add_meal(self, meal):
        self.meal_map[meal.player.index].append(meal)

    def format_cell_list(self, cell_list: List[int]):
        if len(cell_list) == 1:
            return str(cell_list[0])
        return " & ".join(map(str, cell_list))
