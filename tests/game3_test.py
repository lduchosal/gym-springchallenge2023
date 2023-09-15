import unittest
from typing import List

from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.Board import Board
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter


def play(player0_plays: List[str], player1_plays: List[str]):

    Config.MAP_RING_COUNT_MAX = 4
    Config.SCORES_IN_IO = True
    Config.FORCE_SINGLE_HILL = True
    Config.ENABLE_EGGS = False
    Config.MAX_TURNS = False
    game = Game(2)
    player0, player1 = game.players

    info = game.get_global_info_for(player0)
    frame = game.get_current_frame_info_for(player0)
    plot(game.board)

    while not game.game_end:
        cmd0 = player0_plays[game.game_turn] if game.game_turn < len(player0_plays) else "WAIT"
        cmd1 = player1_plays[game.game_turn] if game.game_turn < len(player1_plays) else "WAIT"
        game.handle_player_commands(player0, cmd0)
        game.handle_player_commands(player1, cmd1)
        game.perform_game_update()

        info = game.get_global_info_for(player0)
        frame = game.get_current_frame_info_for(player0)

        if game.game_turn % 10:
            print(game.game_summary_manager)
            plot(game.board)

    plot(game.board)
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
        play0_blue = [
            "LINE 6 10 1",
        ]

        play1_red = [
            "BEACON 5 1;BEACON 11 1;BEACON 9 1",
        ]
        play(play0_blue, play1_red)



if __name__ == '__main__':
    unittest.main()
