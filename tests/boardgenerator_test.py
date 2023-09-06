import unittest
import javarandom
from springchallenge2023.envs.BoardGenerator import BoardGenerator
from springchallenge2023.envs.CellType import CellType
from springchallenge2023.envs.Player import Player

class TestBoardGenerator(unittest.TestCase):

    def test_cell_type(self):

        food = CellType.FOOD
        self.assertEqual(food, CellType.FOOD, f"Food is not None {food}")

    def test_generate_board(self):
        jrandom = javarandom.Random(10)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        board = BoardGenerator.generate(jrandom, players)
        self.assertIsNotNone(board, "Board should not be None")

    def test_is_valid_board(self):
        jrandom = javarandom.Random(10)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        board = BoardGenerator.generate(jrandom, players)
        board_size = len(board.cells)  # Assuming this method exists
        self.assertEqual(5, board_size, "Generated board should be 5")


    def test_is_valid_board(self):
        jrandom = javarandom.Random(10)  # Instantiate your compatible Java random generator
        players = [Player(0), Player(1)]  # Replace with actual Player instances

        board = BoardGenerator.generate(jrandom, players)
        self.assertEqual(CellType.FOOD, board.get_cell_by_index(0).type, "cell0 FOOD")
        self.assertEqual(0, board.get_cell_by_index(0).index, "cell0 index")
        self.assertEqual(0, board.get_cell_by_index(0).coord.x, "cell0 x")
        self.assertEqual(0, board.get_cell_by_index(0).coord.y, "cell0 y")
        self.assertEqual(0, board.get_cell_by_index(0).coord.z, "cell0 z")
        self.assertEqual(49, board.get_cell_by_index(0).richness, "cell0 richness")
        self.assertEqual(None, board.get_cell_by_index(0).anthill, "cell0 anthill")

        self.assertEqual(CellType.EMPTY, board.get_cell_by_index(1).type, "cell1 is EMPTY")
        self.assertEqual(1, board.get_cell_by_index(1).anthill.index, "cell1 anthill")

        self.assertEqual(CellType.EMPTY, board.get_cell_by_index(2).type, "cell2 is FOOD")
        self.assertEqual(CellType.EMPTY, board.get_cell_by_index(3).type, "cell3 is EMPTY")

        self.assertEqual(CellType.EMPTY, board.get_cell_by_index(4).type, "cell4 is EMPTY")
        self.assertEqual(4, board.get_cell_by_index(4).index, "cell4 is EMPTY")
        self.assertEqual(-2, board.get_cell_by_index(4).coord.x, "cell4 x")
        self.assertEqual(2, board.get_cell_by_index(4).coord.y, "cell4 y")
        self.assertEqual(0, board.get_cell_by_index(4).coord.z, "cell4 z")

        self.assertEqual(-1, board.get_cell_by_index(5).index, "cell5 is NOCELL")
        self.assertEqual(-1, board.get_cell_by_index(6).index, "cell6 is NOCELL")
        self.assertEqual(-1, board.get_cell_by_index(7).index, "cell7 is NOCELL")

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
