import re
from typing import List

from springchallenge2023.pyleague.action.ActionType import ActionType
from springchallenge2023.pyleague.action.BeaconAction import BeaconAction
from springchallenge2023.pyleague.action.LineAction import LineAction
from springchallenge2023.pyleague.action.MessageAction import MessageAction
from springchallenge2023.pyleague.action.WaitAction import WaitAction
from springchallenge2023.pyleague.game.Player import Player


class CommandManager:

    def parse_commands(self, player: Player, line: str):
        commands = line.split(";")
        for command in commands:
            command = command.strip()
            found = False
            for action_type in ActionType:
                pattern = action_type.get_pattern()
                match = re.match(pattern, command)
                if match:
                    if action_type == ActionType.BEACON:
                        index = int(match.group("index"))
                        power = int(match.group("power"))
                        action = BeaconAction(index, power)
                    elif action_type == ActionType.LINE:
                        from_index = int(match.group("from"))
                        to_index = int(match.group("to"))
                        ants = int(match.group("ants"))
                        action = LineAction(from_index, to_index, ants)
                    elif action_type == ActionType.MESSAGE:
                        message = match.group("message")
                        action = MessageAction(message)
                    elif action_type == ActionType.WAIT:
                        action = WaitAction()
                    else:
                        action = None

                    player.add_action(action)
                    found = True
                    break

            if not found:
                raise Exception("Invalid command")



