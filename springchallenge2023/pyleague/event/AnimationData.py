class AnimationData:
    def __init__(self, start: int, duration: int):
        self.start: int = start
        self.end: int = start + duration
