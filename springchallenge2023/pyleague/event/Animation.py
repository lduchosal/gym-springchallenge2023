from typing import List

from springchallenge2023.pyleague.event.AnimationData import AnimationData


class Animation:
    HUNDREDTH = 10
    TWENTIETH = 50
    TENTH = 100
    THIRD = 300
    HALF = 500
    WHOLE = 1000

    def __init__(self) -> None:
        self.frame_time = 0
        self.end_time = 0

    def reset(self) -> None:
        self.frame_time = 0
        self.end_time = 0

    def wait(self, time: int) -> int:
        self.frame_time += time
        return self.frame_time

    def get_frame_time(self) -> int:
        return self.frame_time

    def start_anim(self, anim_data: List['AnimationData'], duration: int) -> None:
        anim_data.append(AnimationData(self.frame_time, duration))
        self.end_time = max(self.end_time, self.frame_time + duration)

    def wait_for_anim(self, anim_data: List['AnimationData'], duration: int) -> None:
        anim_data.append(AnimationData(self.frame_time, duration))
        self.frame_time += duration
        self.end_time = max(self.end_time, self.frame_time)

    def chain_anims(self, count: int, anim_data: List['AnimationData'], duration: int, separation: int,
                    wait_for_end: bool = True) -> None:
        for i in range(count):
            anim_data.append(AnimationData(self.frame_time, duration))
            if i < count - 1:
                self.frame_time += separation
        self.end_time = max(self.end_time, self.frame_time + duration)
        if wait_for_end and count > 0:
            self.frame_time += duration

    def set_frame_time(self, start_time: int) -> None:
        self.frame_time = start_time

    def get_end_time(self) -> int:
        return self.end_time

    def catch_up(self) -> None:
        self.frame_time = self.end_time

    def compute_events(self) -> int:
        min_time = 1000
        self.catch_up()
        self.frame_time = max(self.get_frame_time(), min_time)
        return self.frame_time
