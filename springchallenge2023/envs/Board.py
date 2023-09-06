import heapq
from collections import OrderedDict, deque
from functools import cmp_to_key

from springchallenge2023.envs.CubeCoord import CubeCoord
from springchallenge2023.envs.Cell import Cell
from springchallenge2023.envs.CellType import CellType
from springchallenge2023.envs.Player import Player


class Board:
    players: [Player]
    ring_count: int
    cells: [Cell]
    coords: [CubeCoord]

    def __init__(self, mapv, ring_count: int, players: [Player]):
        self.players = players
        self.map = mapv
        self.ring_count = ring_count
        self.cells = sorted(mapv.values(), key=lambda cell: cell.index)
        self.coords = [cell.coord for cell in self.cells]
        self.distance_cache = [[0 for _ in range(len(self.map))] for _ in range(len(self.map))]
        self.attack_cache = [OrderedDict() for _ in players]

    def get_neighbours_by_index(self, i):
        return [self.map[coord].index for coord in self.get_neighbours(self.coords[i])]

    def get_neighbours(self, coord) -> [CubeCoord]:
        return [neighbor for neighbor in coord.neighbours() if neighbor in self.map]

    def get_neighbour_cells(self, cell) -> [Cell]:
        return [self.map.get(coord, Cell.NO_CELL) for coord in self.get_neighbours(cell.coord)]

    def get_neighbour_ids(self, coord) -> str:
        ordered_neighbor_ids = []
        for i in range(len(CubeCoord.directions)):
            ordered_neighbor_ids.append(
                self.map.get(coord.neighbor(i), Cell.NO_CELL).index
            )
        return " ".join(map(str, ordered_neighbor_ids))

    def get_edges(self):
        center = CubeCoord.CENTER
        return [coord for coord in self.coords if coord.distance_to(center) == self.ring_count]

    def get_cell_by_coord(self, coord: CubeCoord):
        return self.map.get(coord, Cell.NO_CELL)

    def get_cell_by_index(self, index: int) -> Cell:
        if index < 0 or index >= len(self.coords):
            return Cell.NO_CELL
        return self.map.get(self.coords[index])

    # Assuming distanceCache is already initialized in __init__
    def get_distance(self, ai, bi):
        if ai == bi:
            return 0

        cached = self.distance_cache[ai][bi]
        if cached > 0:
            return cached

        a, b = self.coords[ai], self.coords[bi]
        distance = self.internal_get_distance(a, b, None)
        self.distance_cache[ai][bi] = distance
        self.distance_cache[bi][ai] = distance
        return distance

    def internal_get_distance(self, a, b, player_idx):
        path = self.find_shortest_path(self.map[a].index, self.map[b].index, player_idx)
        if path is None:
            return -1
        return len(path) - 1

    def find_shortest_path(self, a, b, player_idx=None):
        # BFS
        queue = deque()
        prev = {a: None}

        queue.append(a)

        while queue:
            if b in prev:
                break
            head = queue.popleft()

            neighbours = self.get_neighbours(head)

            if player_idx is not None:
                # Sort neighbours by custom conditions
                neighbours.sort(key=cmp_to_key(lambda x, y: (
                        self.cells[y].get_ants(player_idx) - self.cells[x].get_ants(player_idx) or
                        self.cells[y].get_beacon_power(player_idx) - self.cells[x].get_beacon_power(player_idx) or
                        x - y
                )))
            else:
                # Sort neighbours by cell ID
                neighbours.sort()

            for neighbour in neighbours:
                cell = self.cells[neighbour]
                visited = neighbour in prev
                if cell.is_valid() and not visited:
                    prev[neighbour] = head
                    queue.append(neighbour)

        if b not in prev:
            return None  # Impossibru

        # Reconstruct path
        path = deque()
        current = b
        while current is not None:
            path.appendleft(current)
            current = prev[current]

        return path

    def get_best_path_bycell(self, start, end, player_idx, interrupted_by_fight):
        # Assuming you have a method that converts from index to the best path
        return self.get_best_path_byindex(start.get_index(), end.get_index(), player_idx, interrupted_by_fight)

    attack_cache = []
    initial_food = 0

    def get_attack_power(self, cell_idx, player_idx):
        if cell_idx in self.attack_cache[player_idx]:
            return self.attack_cache[player_idx][cell_idx]

        anthills = self.players[player_idx].anthills

        all_paths = []
        for anthill in anthills:
            best_path = self.get_best_path_byindex(cell_idx, anthill, player_idx, False)

            if best_path:
                all_paths.append(best_path)

        max_min = max(
            min(cell.get_ants(player_idx) for cell in path) if path else 0
            for path in all_paths
        ) if all_paths else 0

        self.attack_cache[player_idx][cell_idx] = max_min
        return max_min

    def reset_attack_cache(self):
        for cache in self.attack_cache:
            cache.clear()

    def get_best_path_byindex(self, start: int, end: int, player_idx: int, interrupted_by_fight: bool):
        max_path_values = [float('-inf')] * len(self.cells)
        prev = [-1] * len(self.cells)
        distance_from_start = [0] * len(self.cells)
        visited = [False] * len(self.cells)

        def compare_values(cell_idx):
            return max_path_values[cell_idx], distance_from_start[cell_idx] + self.get_distance(cell_idx, end)

        queue = []
        start_cell = self.cells[start]
        max_path_values[start] = start_cell.get_ants(player_idx)
        distance_from_start[start] = 0
        start_ants = start_cell.get_ants(player_idx)

        if interrupted_by_fight:
            my_force = self.get_attack_power(start, player_idx)
            other_force = self.get_attack_power(start, 1 - player_idx)
            if other_force > my_force:
                start_ants = 0

        if start_ants > 0:
            heapq.heappush(queue, (-max_path_values[start], start))

        while queue and not visited[end]:
            _, current_idx = heapq.heappop(queue)
            visited[current_idx] = True

            for neighbor in self.get_neighbours(self.get(current_idx)):
                neighbor_idx = neighbor.get_index()
                neighbor_ants = neighbor.get_ants(player_idx)

                if interrupted_by_fight:
                    my_force = self.get_attack_power(neighbor_idx, player_idx)
                    other_force = self.get_attack_power(neighbor_idx, 1 - player_idx)
                    if other_force > my_force:
                        neighbor_ants = 0

                if not visited[neighbor_idx] and neighbor_ants > 0:
                    potential_max_path_value = min(max_path_values[current_idx], neighbor_ants)

                    if potential_max_path_value > max_path_values[neighbor_idx]:
                        max_path_values[neighbor_idx] = potential_max_path_value
                        distance_from_start[neighbor_idx] = distance_from_start[current_idx] + 1
                        prev[neighbor_idx] = current_idx
                        heapq.heappush(queue, (-max_path_values[neighbor_idx], neighbor_idx))

        if not visited[end]:
            return None

        path = []
        current_idx = end
        while current_idx != -1:
            path.insert(0, self.get(current_idx))
            current_idx = prev[current_idx]

        return path

    @staticmethod
    def is_connected_static(coords: [CubeCoord]):
        coords_set = set(coords)
        visited = set()
        stack = []

        start = coords[0]
        stack.append(start)
        visited.add(start)

        while stack:
            coord = stack.pop()
            for neighbor in coord.neighbours():
                if neighbor in coords_set and neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)

        return len(visited) == len(coords)

    def is_connected(self):
        return Board.is_connected_static(self.coords)

    def get_food_cells(self):
        return [cell for cell in self.map.values() if cell.type == CellType.FOOD and cell.richness > 0]

    def get_remaining_food(self):
        return sum(cell.richness for cell in self.map.values() if cell.type == CellType.FOOD)

    def get_egg_cells(self):
        return [cell for cell in self.map.values() if cell.type == CellType.EGG and cell.richness > 0]

    def get_initial_food(self):
        return self.initial_food
