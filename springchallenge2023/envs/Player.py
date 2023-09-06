from typing import List

from springchallenge2023.envs.Action import Action


class Player:

    points: int
    anthills: [int]
    message: str
    index: int

    def __init__(self, index: int):
        self.points = 0
        self.anthills = []
        self.beacons = []
        self.lines = []
        self.message = ""
        self.index = index

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

    def add_action(self, action: Action):
        action_type = action.get_type()
        if action_type == "BEACON":
            self.beacons.append(action)
        elif action_type == "LINE":
            self.lines.append(action)
        elif action_type == "MESSAGE":
            self.set_message(action.get_message())

    def add_anthill(self, index: int):
        self.anthills.append(index)

    def get_anthills(self) -> List[int]:
        return self.anthills

    def add_points(self, n: int):
        self.points += n

    def get_points(self) -> int:
        return self.points

    def get_index(self) -> int:
        return self.index
