import unittest

import javarandom
from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.BoardGenerator import BoardGenerator
from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.FlatBoardPlotter import FlatBoardPlotter
from springchallenge2023.pyleague.game.Player import Player
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter


class TestBoardPlotter(unittest.TestCase):
    def test_cell_type(self):
        neighbors_cube = [
            (0, 0, 0),

            (1, 0, -1), (-1, 0, 1),
            (1, -1, 0), (-1, 1, 0),
            (0, -1, 1), (0, 1, -1),

            (2, 0, -1), (-2, 0, 1),
            (2, -1, 0), (-2, 1, 0),
            (1, -1, 1), (-1, 1, -1),

        ]

        neighbors_cube2 = [
            (0, 0, 0),
            (1, -1, 0),
            (-1, 1, 0),
            (2, -2, 0),
            (-2, 2, 0),
        ]

        fig, axs = plt.subplots(2, 1, figsize=(10, 18))

        bplot = FlatBoardPlotter()
        bplot.hexagon_grid(axs[0], neighbors_cube)
        bplot.hexagon_grid(axs[1], neighbors_cube2)
        plt.show()

    def test_plot_CubeCoord_orientation(self):
        neighbors_cube = CubeCoord.directions
        neighbors_cube2 = neighbors_cube[::-1]

        fig, axs = plt.subplots(2, 1, figsize=(10, 18))

        bplot = FlatBoardPlotter()
        bplot.hexagon_grid(axs[0], neighbors_cube)
        bplot.hexagon_grid(axs[1], neighbors_cube2)
        plt.show()


    def test_print_board(self):
        jrandom = javarandom.Random(100)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        bplot = FlatBoardPlotter()
        board = BoardGenerator.generate(jrandom, players)
        neightscoords = [cell.coord for cell in board.cells]
        neights = [(coord.x, coord.y, coord.z) for coord in neightscoords]
        fig, ax = plt.subplots()
        bplot.hexagon_grid(ax, neights)
        plt.show()




    def test_print_board_random(self):
        jrandom = javarandom.Random(10)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        bplot = FlatBoardPlotter()
        board = BoardGenerator.generate(jrandom, players)
        neightscoords = [cell.coord for cell in board.cells]
        neights = [(coord.x, coord.y, coord.z) for coord in neightscoords]
        fig, ax = plt.subplots(figsize=(20, 14))
        bplot.hexagon_grid(ax, neights)
        plt.show()


    def test_plot_board_random(self):
        jrandom = javarandom.Random(1)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances
        fig, ax = plt.subplots()


        board = BoardGenerator.generate(jrandom, players)
        bplot = FlatBoardPlotter()
        bplot.plot_board(ax, board)
        plt.show()


    def test_plot_pointy_board_random(self):
        jrandom = javarandom.Random(12)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        board = BoardGenerator.generate(jrandom, players)
        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, board)
        plt.show()

    def test_generate_board(self):
        jrandom = javarandom.Random(12)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances
        board = BoardGenerator.generate(jrandom, players)

    def test_generate_board_10(self):
        jrandom = javarandom.Random(10)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances
        board = BoardGenerator.generate(jrandom, players)
        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_board(ax, board)
        plt.show()


    def test_generate_huge_board(self):
        jrandom = javarandom.Random(12)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances
        board = BoardGenerator.generate(jrandom, players)


    # Add more tests as needed
if __name__ == '__main__':
    unittest.main()

