from collections import defaultdict
from typing import List

import javarandom
from javarandom import Random

from springchallenge2023.pyleague.event.Animation import Animation
from springchallenge2023.pyleague.event.EventData import EventData
from springchallenge2023.pyleague.game.AntAllocater import AntAllocater
from springchallenge2023.pyleague.game.AntConsumption import AntConsumption
from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.BoardGenerator import BoardGenerator
from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.CommandManager import CommandManager
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.GameSummaryManager import GameSummaryManager
from springchallenge2023.pyleague.game.Player import Player


class Game:
    random: Random = None

    def __init__(self, seed: int):
        self.game_summary: str = ''
        self.players: List[Player] = [Player(0), Player(1)]
        self.random: Random = javarandom.Random(seed)
        self.game_turn: int = 0
        self.game_end: bool = False
        self.board: Board = BoardGenerator.generate(self.random, self.players)
        self.command_manager: CommandManager = CommandManager()
        self.game_summary_manager: GameSummaryManager = GameSummaryManager()
        self.animation: Animation = Animation()
        self.viewer_events: List[EventData] = []

    def get_board_cells_coord(self) -> [(Cell, CubeCoord)]:
        return [(self.board.get_cell_by_coord(coord), coord) for coord in self.board.coords]

    def get_global_info_for(self, player):
        lines = [str(len(self.board.coords))]
        for coord in self.board.coords:
            cell = self.board.map[coord]
            cell_type = 1 if cell.get_type() == CellType.EGG else 2 if cell.get_type() == CellType.FOOD else 0
            lines.append(f"{cell_type} {cell.get_richness()} {self.board.get_neighbour_ids(coord)}")

        other = self.get_opponent(player)
        lines.append(str(len(player.anthills)))
        lines.append(" ".join(map(str, player.anthills)))
        lines.append(" ".join(map(str, other.anthills)))

        return lines

    def get_current_frame_info_for(self, player) -> [str]:
        lines = []
        other = self.get_opponent(player)
        if Config.SCORES_IN_IO:
            lines.append(" ".join(map(str, [player.points, other.points])))

        for coord in self.board.coords:
            cell = self.board.get_cell_by_coord(coord)
            lines.append(" ".join(
                map(str, [cell.get_richness(), cell.get_ants_by_player(player), cell.get_ants_by_player(other)])))

        return lines

    def handle_player_commands(self, player: Player, command: str):
        self.command_manager.parse_commands(player, command)

    def get_opponent(self, player: Player) -> Player:
        return self.players[1 - player.index]

    def reset_game_turn_data(self):

        for cell in self.board.cells:
            cell.remove_beacons()

        for player in self.players:
            player.reset()

        self.board.reset_attack_cache()

    def perform_game_update(self):
        self.do_lines()
        self.do_beacons()
        self.do_move()

        # self.animation.catch_up()

        # if self.move_animated_this_turn:
        #    self.animation.wait(Animation.THIRD)

        self.do_fights()
        self.do_build()
        # self.animation.catch_up()
        self.board.reset_attack_cache()
        self.do_score()

        # self.animation.catch_up()
        self.game_turn += 1

        if self.check_game_over():
            self.game_end = True

        self.game_summary = str(self.game_summary_manager)
        self.game_summary_manager.clear()

        # frame_time = self.animation.compute_events()
        # self.game_manager.set_frame_duration(frame_time)

    def do_lines(self):

        for player in self.players:
            for line in player.lines:
                from_index = line.from_index
                to_index = line.to_index
                beacon_power = line.ants

                if not self.board.get_cell_by_index(from_index).is_valid():
                    self.game_summary_manager.add_error(
                        player, f"cannot find cell {from_index}"
                    )
                    continue

                if not self.board.get_cell_by_index(to_index).is_valid():
                    self.game_summary_manager.add_error(
                        player, f"cannot find cell {to_index}"
                    )
                    continue

                path = self.board.find_shortest_path(from_index, to_index)
                for cell_index in path:
                    self.set_beacon_power(cell_index, player, beacon_power)

    def do_beacons(self):
        for player in self.players:
            for beacon in player.beacons:
                cell_idx = beacon.cell_index
                power = beacon.power
                self.set_beacon_power(cell_idx, player, power)

    def set_beacon_power(self, cell_index, player, power):
        cell = self.board.get_cell_by_index(cell_index)
        if not cell.is_valid():
            self.game_summary_manager.add_error(
                player, f"cannot find cell {cell_index}"
            )
            return
        cell.set_beacon_power(player.index, max(1, power))

    def do_move(self):

        for player in self.players:

            player_ant_cells = self.get_player_ant_cells(player)
            player_beacon_cells = self.get_player_beacon_cells(player)
            allocations = AntAllocater.allocate_ants(player_ant_cells, player_beacon_cells, player.index, self.board)

            moves = defaultdict(int)

            for alloc in allocations:
                # Get next step in path
                path = self.board.find_shortest_path(alloc.ant_index, alloc.beacon_index, player.index)

                if len(path) > 1:
                    neighbor = path[1]
                    ant_move = (alloc.ant_index, neighbor)
                    moves[ant_move] += alloc.amount

            for move, amount in moves.items():
                self.apply_move(move[0], move[1], amount, player.index)

    def apply_move(self, from_idx: int, to_idx: int, amount: int, player_idx: int):
        source = self.board.get_cell_by_index(from_idx)
        target = self.board.get_cell_by_index(to_idx)

        source.remove_ants_by_idx(player_idx, amount)
        target.place_ants_by_idx(player_idx, amount)

    def get_player_ant_cells(self, player: Player):
        return [cell for cell in self.board.cells if cell.get_ants_by_player(player) > 0]

    def get_player_beacon_cells(self, player: Player):
        return [cell for cell in self.board.cells if cell.get_beacon_power_by_player(player) > 0]

    def do_fights(self):
        if Config.FIGHTING_ANTS_KILL:
            for coord in self.board.coords:
                cell = self.board.get_cell_by_coord(coord)
                ants0 = cell.get_ants(0)
                ants1 = cell.get_ants(1)
                cell.remove_ants(0, min(Config.MAX_ANT_LOSS, ants1))
                cell.remove_ants(1, min(Config.MAX_ANT_LOSS, ants0))

    def do_build(self):
        egg_cells = self.board.get_egg_cells()
        builds = []
        for player in self.players:
            builds.extend(self.compute_cell_consumption(player, egg_cells))

        for build in builds:
            for idx in build.player.anthills:
                self.board.get_cell_by_index(idx).place_ants_by_player(build.player, build.amount)

            self.launch_build_event(build.amount, build.player.index, build.path)
            build.cell.deplete(build.amount)
            self.game_summary_manager.add_build(build)

    def compute_cell_consumption(self, player: Player, target_cells: [Cell]):
        anthills = player.get_anthills()
        meals = []

        for food_cell in target_cells:
            all_paths = []
            for anthill in anthills:
                anthill_cell = self.board.get_cell_by_index(anthill)
                best_path_to_hill = self.board.get_best_path_bycell(food_cell, anthill_cell, player.index,
                                                                    Config.LOSING_ANTS_CANT_CARRY)

                if best_path_to_hill is not None:
                    all_paths.append(best_path_to_hill)

            def by_path_value(path):
                return self.path_value(player, path)

            # Sort by path_value in descending order, then by list size in ascending order
            sorted_paths = sorted(all_paths, key=lambda x: (-by_path_value(x), len(x)))
            best_path = sorted_paths[0] if sorted_paths else None

            max_min = by_path_value(best_path) if best_path else 0
            food_eaten = min(max_min, food_cell.get_richness())

            if food_eaten > 0:
                meals.append(AntConsumption(player, food_eaten, food_cell, best_path))

        return meals

    def path_value(self, player: Player, cell_list: List[Cell]) -> int:
        return min((cell.get_ants_by_player(player) for cell in cell_list), default=0)

    def launch_move_event(self, from_idx: int, to_idx: int, amount: int, player_idx: int) -> None:
        e = EventData()
        e.type = EventData.MOVE
        e.player_idx = player_idx
        e.cell_idx = from_idx
        e.target_idx = to_idx
        e.amount = amount
        self.animation.start_anim(e.anim_data, Animation.HALF)
        self.viewer_events.append(e)

    def launch_build_event(self, amount: int, player_idx: int, path: List[Cell]) -> None:
        e = EventData()
        e.type = EventData.BUILD
        e.player_idx = player_idx
        e.amount = amount
        e.path = [cell.get_index() for cell in path]
        self.animation.start_anim(e.anim_data, Animation.HALF)
        self.viewer_events.append(e)

    def do_score(self):
        food_cells = self.board.get_food_cells()
        meals = []
        for player in self.players:
            meals.extend(self.compute_cell_consumption(player, food_cells))

        for meal in meals:
            self.launch_food_event(meal)
            self.game_summary_manager.add_meal(meal)

            meal.player.add_points(meal.amount)
            meal.cell.deplete(meal.amount)

    def launch_food_event(self, meal: AntConsumption):
        e = EventData()
        e.type = EventData.FOOD
        e.player_idx = meal.player.index
        e.path = [cell.get_index() for cell in meal.path]
        e.amount = meal.amount
        self.animation.start_anim(e.anim_data, Animation.HALF)
        self.viewer_events.append(e)

    def check_game_over(self) -> bool:
        remaining_food = self.board.get_remaining_food()

        if remaining_food == 0:
            self.game_summary_manager.add_no_more_food()
            return True
        if self.players[0].points >= self.players[1].points + remaining_food:
            self.game_summary_manager.add_not_enough_food_left(self.players[0])
            return True
        elif self.players[1].points >= self.players[0].points + remaining_food:
            self.game_summary_manager.add_not_enough_food_left(self.players[1])
            return True
        return False
