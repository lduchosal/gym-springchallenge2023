# Assuming the enum values are defined elsewhere
from springchallenge2023.envs.ActionType import ActionType


class Action:

    def __init__(self, action_type: ActionType):
        self.type = action_type

    def get_type(self) -> ActionType:
        return self.type
