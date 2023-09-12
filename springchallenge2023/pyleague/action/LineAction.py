# Assuming the enum values are defined elsewhere
from springchallenge2023.pyleague.action.ActionType import ActionType


class LineAction:

    def __init__(self, from_index: int, to_index: int, ants: int):
        self.type = ActionType.LINE
        self.from_index = from_index
        self.to_index = to_index
        self.ants = ants
