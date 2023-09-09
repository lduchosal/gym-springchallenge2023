import unittest

import javarandom
from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.BoardGenerator import BoardGenerator
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.FlatBoardPlotter import FlatBoardPlotter
from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.game.Player import Player
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter


class TestGame(unittest.TestCase):
    def test1(self):
        Config.MAP_RING_COUNT_MAX = 10
        game = Game(10)
        info = game.getGlobalInfoFor(game.players[0])
        self.assertEqual(info[0], "5", "nbcells")
        self.assertEqual(info[1], "0 49 1 -1 -1 2 -1 -1", "0")
        self.assertEqual(info[2], "0 0 3 -1 -1 0 -1 -1", "1")
        self.assertEqual(info[3], "0 0 0 -1 -1 4 -1 -1", "2")
        self.assertEqual(info[4], "0 0 -1 -1 -1 1 -1 -1", "3")
        self.assertEqual(info[5], "0 0 2 -1 -1 -1 -1 -1", "4")

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()


    def test2(self):
        Config.MAP_RING_COUNT_MAX = 10
        game = Game(12)
        info = game.getGlobalInfoFor(game.players[0])
        self.assertEqual(info[0], "45", "nbcells")

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, game.board)
        plt.show()

        self.assertEqual(info[1], "0 0 1 3 5 2 4 6", "0")
        self.assertEqual(info[2], "0 11 7 9 3 0 6 16", "1")
        self.assertEqual(info[3], "0 11 0 5 15 8 10 4", "2")
        self.assertEqual(info[4], "0 0 9 -1 11 5 0 1", "3")
        self.assertEqual(info[5], "0 0 6 0 2 10 -1 12", "4")


    # Add more tests as needed
if __name__ == '__main__':
    unittest.main()

