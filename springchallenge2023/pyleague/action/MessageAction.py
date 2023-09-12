from springchallenge2023.pyleague.action import ActionType


class MessageAction:

    def __init__(self, message):
        self.type = ActionType.MESSAGE
        self.message = message
