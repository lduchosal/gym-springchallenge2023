import unittest

from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter


class TestGame(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def test_get_current_frame_info_for_10(self):
        Config.MAP_RING_COUNT_MAX = 10
        game = Game(10)
        info = game.get_global_info_for(game.players[0])
        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(9, len(info), "infos")

        self.assertEqual(info[0], "5", "nbcells")
        self.assertEqual(info[1], "2 49 1 -1 -1 2 -1 -1", "0")
        self.assertEqual(info[2], "0 0 3 -1 -1 0 -1 -1", "1")
        self.assertEqual(info[3], "0 0 0 -1 -1 4 -1 -1", "2")
        self.assertEqual(info[4], "0 0 -1 -1 -1 1 -1 -1", "3")
        self.assertEqual(info[5], "0 0 2 -1 -1 -1 -1 -1", "4")

        self.assertEqual(info[6], "1", "anthills")
        self.assertEqual(info[7], "2", "my anthill")
        self.assertEqual(info[8], "1", "opp anthill")

    def test_get_current_frame_info_for_12(self):
        Config.MAP_RING_COUNT_MAX = 10
        game = Game(12)
        info = game.get_global_info_for(game.players[0])
        self.assertEqual(info[0], "45", "nbcells")

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(info[1], "0 0 1 3 5 2 4 6", "0")
        self.assertEqual(info[2], "1 11 7 9 3 0 6 -1", "1")
        self.assertEqual(info[3], "1 11 0 5 -1 8 10 4", "2")
        self.assertEqual(info[4], "0 0 9 11 13 5 0 1", "3")
        self.assertEqual(info[5], "0 0 6 0 2 10 12 14", "4")
        self.assertEqual(info[6], "2 5 3 13 -1 -1 2 0", "4")
        self.assertEqual(info[7], "2 5 -1 1 0 4 14 -1", "4")

    def test_get_current_frame_info_for(self):
        Config.MAP_RING_COUNT_MAX = 10
        Config.SCORES_IN_IO = False
        game = Game(10)
        frame = game.get_current_frame_info_for(game.players[0])

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(frame[0], "49 0 0", "0")
        self.assertEqual(frame[1], "0 0 60", "1")
        self.assertEqual(frame[2], "0 60 0", "2")
        self.assertEqual(frame[3], "0 0 0", "3")
        self.assertEqual(frame[4], "0 0 0", "4")

    def test_get_current_frame_info_for(self):
        Config.MAP_RING_COUNT_MAX = 10
        Config.SCORES_IN_IO = True
        game = Game(10)
        frame = game.get_current_frame_info_for(game.players[0])

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(frame[0], "0 0", "score")
        self.assertEqual(frame[1], "49 0 0", "0")
        self.assertEqual(frame[2], "0 0 60", "1")
        self.assertEqual(frame[3], "0 60 0", "2")
        self.assertEqual(frame[4], "0 0 0", "3")
        self.assertEqual(frame[5], "0 0 0", "4")

    def test_get_current_frame_info_for_2(self):
        Config.MAP_RING_COUNT_MAX = 10
        Config.SCORES_IN_IO = True
        game = Game(10)
        frame = game.get_current_frame_info_for(game.players[0])

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(frame[0], "0 0", "score")
        self.assertEqual(frame[1], "49 0 0", "0")
        self.assertEqual(frame[2], "0 0 60", "1")
        self.assertEqual(frame[3], "0 60 0", "2")
        self.assertEqual(frame[4], "0 0 0", "3")
        self.assertEqual(frame[5], "0 0 0", "4")



    def test_perform_game_update(self):
        Config.MAP_RING_COUNT_MAX = 10
        Config.SCORES_IN_IO = True
        game = Game(10)
        player0, player1 = game.players

        info = game.get_global_info_for(player0)
        frame = game.get_current_frame_info_for(player0)

        game.handle_player_commands(player0, "LINE 0 2 10")
        game.handle_player_commands(player1, "LINE 0 1 10")

        game.perform_game_update()

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()


if __name__ == '__main__':
    unittest.main()
