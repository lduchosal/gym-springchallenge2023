from springchallenge2023.pyleague.action import ActionType


class BeaconAction:

    def __init__(self, cell_index, power):
        self.type = ActionType.BEACON
        self.cell_index = cell_index
        self.power = power
