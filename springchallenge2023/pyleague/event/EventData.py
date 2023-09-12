from typing import List, Optional

from springchallenge2023.pyleague.event.AnimationData import AnimationData


class EventData:
    BUILD = 0
    MOVE = 1
    FOOD = 2
    BEACON = 3

    def __init__(self):
        self.type: int = 0
        self.anim_data: List['AnimationData'] = []
        self.player_idx: Optional[int] = None
        self.cell_idx: Optional[int] = None
        self.target_idx: Optional[int] = None
        self.amount: Optional[int] = None
        self.path: Optional[List[int]] = None


