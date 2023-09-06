import re
from enum import Enum


class ActionType(Enum):
    BEACON = re.compile(r"^BEACON (?P<index>\d+) (?P<power>\d+)")
    LINE = re.compile(r"^LINE (?P<from>\d+) (?P<to>\d+) (?P<ants>\d+)")
    MESSAGE = re.compile(r"^MESSAGE (?P<message>.*)")
    WAIT = re.compile(r"^WAIT")

    def get_pattern(self):
        return self.value
