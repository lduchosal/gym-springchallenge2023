from gymnasium import ActionWrapper


class LineAction(ActionWrapper):

    def action(self, action):
        line = "LINE 9 {} 10".format(action[0], action[1])
        return line

    def reverse_action(self, action):
        return action


