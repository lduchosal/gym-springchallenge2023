from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Cell import Cell
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.Player import Player
from javarandom import Random


class BoardGenerator:
    random_instance: Random = None

    @staticmethod
    def generate(random_instance: Random, players: [Player]):
        BoardGenerator.random_instance = random_instance
        board = BoardGenerator.create_empty_board(players)
        BoardGenerator.add_resource_cells(board, players)
        return board

    @staticmethod
    def create_empty_board(players):
        iterations = 1000
        while iterations > 0:
            board = BoardGenerator.generate_potentially_unconnected_graph(players)
            if board.is_connected():
                return board
            iterations -= 1

    # Replace `generate_potentially_unconnected_graph` with your actual function
    @staticmethod
    def generate_potentially_unconnected_graph(players):
        cells = {}
        next_cell_index = 0
        ring_count = BoardGenerator.random_instance.nextInt(
            Config.MAP_RING_COUNT_MAX - Config.MAP_RING_COUNT_MIN + 1) + Config.MAP_RING_COUNT_MIN
        coord_list = set()

        center = CubeCoord.CENTER
        coord_list.add(center)
        cur = center.neighbor(0)
        vertical_limit = int((ring_count * Config.VERTICAL_CUTOFF) + 0.5)

        for distance in range(1, ring_count + 1):
            for orientation in range(6):
                for count in range(distance):
                    if -vertical_limit < cur.z < vertical_limit:
                        if cur not in coord_list:
                            coord_list.update([cur, cur.get_opposite()])
                    cur = cur.neighbor((orientation + 2) % 6)
            cur = cur.neighbor(0)

        coord_list_size = len(coord_list)
        wanted_empty_cells = BoardGenerator.random_percentage(Config.MIN_EMPTY_CELLS_PERCENT,
                                                              Config.MAX_EMPTY_CELLS_PERCENT, len(coord_list))

        to_remove = set()
        while len(to_remove) < wanted_empty_cells:
            rand_index = BoardGenerator.random_instance.nextInt(coord_list_size - 1)
            rand_coord = list(coord_list)[rand_index]
            to_remove.update([rand_coord, rand_coord.get_opposite()])
        coord_list.difference_update(to_remove)  # [x for index, x in enumerate(coord_list) if x not in to_remove]
        corridor_mode = BoardGenerator.random_instance.nextDouble() < 0.05
        if corridor_mode:
            to_remove.clear()
            for index, coord in enumerate(coord_list):
                if BoardGenerator.has_six_neighbours(coord, coord_list):
                    to_remove.add(coord)
            # coord_list = [x for x in coord_list if x not in to_remove]
            coord_list.difference_update(to_remove)

        no_blob_mode = BoardGenerator.random_instance.nextDouble() < 0.70
        if no_blob_mode:
            changed = True
            while changed:
                changed = False
                cell_with_six_neights = (c for index, c in enumerate(coord_list) if
                                         BoardGenerator.has_six_neighbours(c, coord_list))
                blob_center = next(cell_with_six_neights, None)
                if blob_center:
                    neighbours = blob_center.neighbours()
                    BoardGenerator.shuffle(neighbours)
                    coord_list.remove(neighbours[0])
                    coord_list.discard(neighbours[0].get_opposite())
                    changed = True

        for coord in sorted(coord_list, key=lambda c: c.index):
            cell = Cell(next_cell_index, coord)
            next_cell_index += 1
            cells[coord] = cell

        return Board(cells, ring_count, players)

    @staticmethod
    def random_percentage(minv: int, maxv: int, total: int):
        # int percentage = min + random.nextInt((max + 1) - min);
        percentage = minv + BoardGenerator.random_instance.nextInt((maxv + 1) - minv)
        return int((percentage * total) / 100)

    @staticmethod
    def has_six_neighbours(coord: CubeCoord, coord_list: {CubeCoord}):
        has_six = len([c for c in coord.neighbours() if c in coord_list]) == 6
        return has_six

    @staticmethod
    def add_resource_cells(board: Board, players):
        # Fill center cell
        if BoardGenerator.random_instance.nextBoolean():
            center_cell = board.get_cell_by_coord(CubeCoord.CENTER)
            if center_cell != Cell.NO_CELL:
                center_cell.set_food_amount(BoardGenerator.get_large_food_amount())

        # Place anthills
        hills_per_player = 1 if Config.FORCE_SINGLE_HILL else (
            2 if BoardGenerator.random_instance.nextDouble() < 0.33 else 1)

        valid_coords = BoardGenerator.select_anthill_coords(board, hills_per_player)

        player1, player2 = players[0], players[1]
        for i in range(min(hills_per_player, len(valid_coords))):
            coord = valid_coords[i]

            cell1 = board.map.get(coord)
            cell1.set_anthill(player1)
            player1.add_anthill(cell1.index)

            cell2 = board.map.get(coord.get_opposite())
            cell2.set_anthill(player2)
            player2.add_anthill(cell2.index)

        # Place food
        SURPLUS_MODE = True if Config.FORCE_SINGLE_HILL else BoardGenerator.random_instance.nextDouble() < 0.1  # 10% chance
        HUNGRY_MODE = False if Config.FORCE_SINGLE_HILL else (
                not SURPLUS_MODE and BoardGenerator.random_instance.nextDouble() < 0.08)  # 8% chance
        FAMINE_MODE = False if Config.FORCE_SINGLE_HILL else (
                not SURPLUS_MODE and not HUNGRY_MODE and BoardGenerator.random_instance.nextDouble() < 0.04)  # 4% chance

        if not FAMINE_MODE:
            valid_food_coords = [coord for coord in board.coords if
                                 board.get_cell_by_coord(coord).get_anthill() is None]
            wanted_food_cells = BoardGenerator.random_percentage(Config.MIN_FOOD_CELLS_PERCENT,
                                                                 Config.MAX_FOOD_CELLS_PERCENT, len(valid_food_coords))
            wanted_food_cells = max(2, wanted_food_cells)

            BoardGenerator.shuffle(valid_food_coords)
            for i in range(0, wanted_food_cells, 2):
                coord = valid_food_coords[i]
                cell = board.get_cell_by_coord(coord)
                roll = BoardGenerator.random_instance.nextDouble()
                if roll < 0.65:
                    amount = BoardGenerator.get_small_food_amount() if HUNGRY_MODE else BoardGenerator.get_large_food_amount()
                    if SURPLUS_MODE:
                        amount *= 5 if Config.FORCE_SINGLE_HILL else 10
                    cell.set_food_amount(amount)
                    board.get_cell_by_coord(coord.get_opposite()).set_food_amount(amount)
                else:
                    amount = BoardGenerator.get_small_food_amount() if HUNGRY_MODE else BoardGenerator.get_small_food_amount() // 2
                    if SURPLUS_MODE:
                        amount *= 5 if Config.FORCE_SINGLE_HILL else 10
                    cell.set_food_amount(amount)
                    board.get_cell_by_coord(coord.get_opposite()).set_food_amount(amount)

            # Make sure there is food on the board
            board_has_food = any(cell.get_type() == CellType.FOOD for cell in board.cells)
            if not board_has_food:
                empty_cells = [cell for cell in board.cells if
                               cell.get_type() == CellType.EMPTY and cell.is_valid() and cell.get_anthill() is None]
                random_index = BoardGenerator.random_instance.randint(0, len(empty_cells) - 1)
                empty_cell = empty_cells[random_index]
                amount = BoardGenerator.get_large_food_amount()
                if SURPLUS_MODE:
                    amount *= 10
                empty_cell.set_food_amount(amount)
                opposite_cell = board.get_cell_by_coord(empty_cell.get_coord().get_opposite())
                if opposite_cell.get_coord() != empty_cell.get_coord():
                    opposite_cell.set_food_amount(amount)

            # Place eggs if enabled
            ant_potential = 0
            if Config.ENABLE_EGGS:
                valid_egg_coords = [coord for coord in board.coords if
                                    board.get_cell_by_coord(coord).get_anthill() is None and board.get_cell_by_coord(
                                        coord).get_richness() == 0]
                wanted_egg_cells = BoardGenerator.random_percentage(Config.MIN_EGG_CELLS_PERCENT,
                                                                    Config.MAX_EGG_CELLS_PERCENT, len(valid_egg_coords))

                BoardGenerator.shuffle(valid_egg_coords)
                for i in range(0, wanted_egg_cells, 2):
                    coord = valid_egg_coords[i]
                    cell = board.get_cell_by_coord(coord)
                    roll = BoardGenerator.random_instance.nextDouble()
                    if roll < 0.4:
                        amount = BoardGenerator.get_large_eggs_amount()
                        cell.set_spawn_power(amount)
                        board.get_cell_by_coord(coord.get_opposite()).set_spawn_power(amount)
                        ant_potential += amount * 2
                    else:
                        amount = BoardGenerator.get_small_eggs_amount()
                        cell.set_spawn_power(amount)
                        board.get_cell_by_coord(coord.get_opposite()).set_spawn_power(amount)
                        ant_potential += amount * 2

            # Place ants
            ants_per_hill = max(10, 60 - ant_potential)
            for player in players:
                for idx in player.anthills:
                    board.get_cell_by_index(idx).place_ants_by_player(player, ants_per_hill)

            # Set initial food
            board.initial_food = board.get_remaining_food()

    @staticmethod
    def get_small_eggs_amount():
        return 10 + BoardGenerator.random_instance.nextInt(9)

    @staticmethod
    def get_large_eggs_amount():
        return 20 + BoardGenerator.random_instance.nextInt(19)

    @staticmethod
    def get_small_food_amount():
        return 10 + BoardGenerator.random_instance.nextInt(29)

    @staticmethod
    def get_large_food_amount():
        return 40 + BoardGenerator.random_instance.nextInt(19)

    @staticmethod
    def select_anthill_coords(board, hills_per_player):
        valid_coords = []
        iter_count = 1000

        while len(valid_coords) < hills_per_player and iter_count > 0:
            iter_count -= 1
            valid_coords = BoardGenerator.try_select_anthill_coords(board, hills_per_player)

        # Failsafes
        if len(valid_coords) < hills_per_player:
            valid_coords = board.get_edges()

        if len(valid_coords) < hills_per_player:
            valid_coords = board.coords

        return valid_coords

    @staticmethod
    def try_select_anthill_coords(board: Board, starting_hill_count):
        coordinates = []

        available_coords = list(board.coords)
        available_coords = [coord for coord in available_coords if board.get_cell_by_coord(coord).index != 0]
        available_coords = [coord for coord in available_coords if board.get_cell_by_coord(coord).richness <= 0]

        for i in range(starting_hill_count):
            if not available_coords:
                break
            r = BoardGenerator.random_instance.nextInt(len(available_coords))
            normal_coord = available_coords[r]
            opposite_coord = normal_coord.get_opposite()

            available_coords = [coord for coord in available_coords if
                                coord.distance_to(normal_coord) > Config.STARTING_HILL_DISTANCE and
                                coord.distance_to(opposite_coord) > Config.STARTING_HILL_DISTANCE]

            coordinates.append(normal_coord)

        return coordinates

    @staticmethod
    def shuffle(lst):
        rnd = BoardGenerator.random_instance
        SHUFFLE_THRESHOLD = 5  # Assuming some value, replace as needed
        size = len(lst)

        if size < SHUFFLE_THRESHOLD:
            for i in range(size, 1, -1):
                BoardGenerator.swap(lst, i - 1, rnd.nextInt(i))
        else:
            arr = lst.copy()

            # Shuffle array
            for i in range(size, 1, -1):
                BoardGenerator.swap(arr, i - 1, rnd.nextInt(i))

            # Dump array back into list
            for i, e in enumerate(arr):
                lst[i] = e

    @staticmethod
    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]
