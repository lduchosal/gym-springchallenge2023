from typing import List

from springchallenge2023.pyleague.action.ActionType import ActionType
from springchallenge2023.pyleague.action.BeaconAction import BeaconAction
from springchallenge2023.pyleague.action.LineAction import LineAction


class Player:

    def __init__(self, index: int):
        self.points: int = 0
        self.anthills: [int] = []
        self.beacons: [BeaconAction] = []
        self.lines: [LineAction] = []
        self.message: str = ""
        self.index: int = index
        self.name: str = f'Player{index}'

    def __str__(self):
        return f"Player {self.index}"

    def __repr__(self):
        return f"Player{self.index}"

    @staticmethod
    def get_expected_output_lines():
        return 1

    def get_message(self):
        return self.message

    def set_message(self, message: str):
        if message:
            trimmed = message.strip()
            if len(trimmed) > 48:
                trimmed = trimmed[:46] + "..."
            if len(trimmed) > 0:
                self.message = trimmed

    def reset(self):
        self.message = None
        self.beacons.clear()
        self.lines.clear()

    def add_action(self, action):
        action_type = action.type
        if action.type == ActionType.BEACON:
            self.beacons.append(action)
        elif action_type == ActionType.LINE:
            self.lines.append(action)
        elif action_type == ActionType.MESSAGE:
            self.set_message(action.message)

    def add_anthill(self, index: int):
        self.anthills.append(index)

    def get_anthills(self) -> List[int]:
        return self.anthills

    def add_points(self, n: int):
        self.points += n

    def get_points(self) -> int:
        return self.points
