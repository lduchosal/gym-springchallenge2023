import unittest

from springchallenge2023.pyleague.game import CommandManager
from springchallenge2023.pyleague.game import Player


class MyTestCase(unittest.TestCase):
    def test_wait(self):

        command_manager = CommandManager()
        player = Player(0)
        command_manager.parse_commands(player, ["WAIT"])
        self.assertEqual(True, True)  # add assertion here
        self.assertEqual(0, len(player.lines), "lines")  # add assertion here
        self.assertEqual(0, len(player.beacons), "beacons")  # add assertion here
        self.assertEqual('', player.message, "message")  # add assertion here


    def test_line(self):

        command_manager = CommandManager()
        player = Player(0)
        command_manager.parse_commands(player, ["LINE 0 1 10"])
        self.assertEqual(1, len(player.lines), "lines")  # add assertion here
        self.assertEqual(0, len(player.beacons), "beacons")  # add assertion here
        self.assertEqual('', player.message, "message")  # add assertion here


    def test_beacon(self):

        command_manager = CommandManager()
        player = Player(0)
        command_manager.parse_commands(player, ["BEACON 0 10"])
        self.assertEqual(0, len(player.lines), "lines")  # add assertion here
        self.assertEqual(1, len(player.beacons), "beacons")  # add assertion here
        self.assertEqual('', player.message, "message")  # add assertion here

    def test_beacons_2(self):

        command_manager = CommandManager()
        player = Player(0)
        command_manager.parse_commands(player, ["BEACON 0 10; BEACON 1 100"])
        self.assertEqual(0, len(player.lines), "lines")  # add assertion here
        self.assertEqual(2, len(player.beacons), "beacons")  # add assertion here
        self.assertEqual('', player.message, "message")  # add assertion here


    def test_message(self):

        command_manager = CommandManager()
        player = Player(0)
        command_manager.parse_commands(player, ["MESSAGE hello"])
        self.assertEqual(0, len(player.lines), "lines")  # add assertion here
        self.assertEqual(0, len(player.beacons), "beacons")  # add assertion here
        self.assertEqual('hello', player.message, "message")  # add assertion here


if __name__ == '__main__':
    unittest.main()
