import math

from springchallenge2023.pyleague.view.CellData import CellData


class AntAllocater:

    @staticmethod
    def convert(cells, player_idx):
        return [CellData(cell, player_idx) for cell in cells]

    @staticmethod
    def allocate_ants(ant_cells, beacon_cells, player_idx, board):
        return AntAllocater.inner_allocate_ants(
            AntAllocater.convert(ant_cells, player_idx),
            AntAllocater.convert(beacon_cells, player_idx),
            player_idx,
            board
        )

    @staticmethod
    def get_distance(pair, player_idx, board):
        return board.get_distance(pair.ant.cell.get_index(), pair.beacon.cell.get_index())

    @staticmethod
    def inner_allocate_ants(ant_cells, beacon_cells, player_idx, board):
        allocations = []
        ant_sum = sum(cell.ants for cell in ant_cells)
        beacon_sum = sum(cell.beacons for cell in beacon_cells)

        scaling_factor = float('inf')
        if beacon_sum > 0:
            scaling_factor = float(ant_sum) / beacon_sum

        for cell in beacon_cells:
            high_beacon_value = int(math.ceil(cell.beacons * scaling_factor))
            low_beacon_value = int(cell.beacons * scaling_factor)
            cell.beacons = max(1, low_beacon_value)
            cell.wiggle_room = high_beacon_value - cell.beacons

        all_pairs = []

        for ant_cell in ant_cells:
            for beacon_cell in beacon_cells:
                pair = AntBeaconPair(ant_cell, beacon_cell)
                if AntAllocater.get_distance(pair, player_idx, board) != -1:
                    all_pairs.append(pair)

        all_pairs.sort(key=lambda p: (
            AntAllocater.get_distance(p, player_idx, board),
            p.ant.cell.get_index(),
            p.beacon.cell.get_index())
                       )

        stragglers = False

        while all_pairs:
            for pair in all_pairs:
                ant_cell = pair.ant
                ant_count = ant_cell.ants
                beacon_cell = pair.beacon
                beacon_count = beacon_cell.beacons
                wiggle_room = beacon_cell.wiggle_room

                max_alloc = min(
                    ant_count,
                    beacon_count + wiggle_room if stragglers else beacon_count
                )
                if max_alloc > 0:
                    allocations.append(
                        AntAllocation(
                            ant_cell.cell.get_index(),
                            beacon_cell.cell.get_index(),
                            max_alloc
                        )
                    )
                    ant_cell.ants -= max_alloc
                    if not stragglers:
                        beacon_cell.beacons -= max_alloc
                    else:
                        beacon_cell.beacons -= (max_alloc - wiggle_room)
                        beacon_cell.wiggle_room = 0

            all_pairs = [pair for pair in all_pairs if pair.ant.ants > 0]
            stragglers = True

        return allocations


class CellData:
    def __init__(self, cell, player_idx):
        self.cell = cell
        self.ants = cell.get_ants_by_idx(player_idx)
        self.beacons = cell.get_beacon_power_by_idx(player_idx)
        self.wiggle_room = 0


class AntBeaconPair:
    def __init__(self, ant, beacon):
        self.ant = ant
        self.beacon = beacon


class AntAllocation:
    def __init__(self, ant_index, beacon_index, amount):
        self.ant_index = ant_index
        self.beacon_index = beacon_index
        self.amount = amount

