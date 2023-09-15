import unittest
from typing import List

from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter


def play(player0_plays: List[str], player1_plays: List[str]):

    Config.MAP_RING_COUNT_MAX = 11
    Config.SCORES_IN_IO = True
    game = Game(10)
    player0, player1 = game.players

    info = game.get_global_info_for(player0)
    frame = game.get_current_frame_info_for(player0)
    #plot(game.board)

    while not game.game_end:
        cmd0 = player0_plays[game.game_turn] if game.game_turn < len(player0_plays) else "WAIT"
        cmd1 = player1_plays[game.game_turn] if game.game_turn < len(player1_plays) else "WAIT"
        game.handle_player_commands(player0, cmd0)
        game.handle_player_commands(player1, cmd1)
        game.perform_game_update()

        #plot(game.board)

    print(game.game_summary)


def plot(board: Board):


    bplot = PointyBoardPlotter()
    fig, ax = plt.subplots(figsize=(1024 / 100, 768 / 100), dpi=150)
    bplot.plot_board(ax, board)
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.show()

class TestGame(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def test_perform_game_update(self):
        play0 = [
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
            "LINE 11 25 1;LINE 11 27 1;LINE 11 14 1;LINE 11 22 1;LINE 11 16 1;LINE 11 8 1;LINE 11 3 1;LINE 11 4 1",
        ]

        play1 = [
            "BEACON 12 1;BEACON 4 1;BEACON 26 1;BEACON 28 1;BEACON 21 1;BEACON 13 1;BEACON 18 1",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "WAIT",
            "BEACON 6666 1;BEACON 4 1;BEACON 2 1;BEACON 8 1;BEACON 16 1;BEACON 20 1;BEACON 21 1;BEACON 13 1;BEACON 18 1;BEACON 15 1;BEACON 7 1",
        ]
        play(play0, play1)



if __name__ == '__main__':
    unittest.main()
