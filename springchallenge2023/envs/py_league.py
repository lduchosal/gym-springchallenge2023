import logging

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.CellType import CellType
from springchallenge2023.pyleague.game.Config import Config
from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter



class PyLeagueEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode: str = None):
        super(PyLeagueEnv, self)
        print("PyLeagueEnv __init__")

        self.renderer = PointyBoardPlotter() if render_mode == 'human' else None

        # Define action and observation space
        # celltype, eggs, crystal, myants, oppants
        self.observation_space = spaces.Box(
            low=np.zeros((15, 5), dtype=int),
            high=np.full((15, 5), 300, dtype=int),
            dtype=int)

        # actions is a [10, 10,100], user actionwrappers
        self.action_space = spaces.Box(
            low=np.zeros((15,), dtype=float),
            high=np.ones((15,), dtype=float),
            dtype=float)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

        # Initialize state
        self.state = None
        self.prev_reward0 = 0
        self.prev_reward1 = 0

        Config.MAP_RING_COUNT_MAX = 4
        Config.SCORES_IN_IO = True
        Config.FORCE_SINGLE_HILL = True
        Config.ENABLE_EGGS = False
        Config.MAX_TURNS = False

        self.game = None

    def step(self, action):
        # Implement your step logic here
        reward = 0
        logging.debug(f"action: {action}")

        player0 = self.game.players[0]
        player1 = self.game.players[1]

        nactions = [int(value*10) for value in action]
        cmd0 = ';'.join([f'BEACON {i} {value}' for i, value in enumerate(nactions) if value > 0])
        cmd1 = ';'.join([f'BEACON {i} 1' for i in range(15)])

        self.game.handle_player_commands(player0, cmd0)
        self.game.handle_player_commands(player1, cmd1)

        self.game.perform_game_update()

        info = self.game.get_global_info_for(player0)
        frame = self.game.get_current_frame_info_for(player0)
        summary = self.game.game_summary

        extra = {'info': info, 'frame': frame, 'summary': summary }

        terminated = self.game.game_end
        truncated = False

        reward0 = player0.get_points()
        reward1 = player1.get_points()
        reward = (reward0 - self.prev_reward0) - (reward1 - self.prev_reward1)

        self.prev_reward0 = reward0
        self.prev_reward1 = reward1

        if terminated:
            reward = 100 if reward0 > reward1 else -100

        self.state = self.obs()

        logging.debug(f"state: {self.state}")
        logging.debug(f"info: {extra}")
        logging.debug(f"reward: {reward}")

        return self.state, reward, terminated, truncated, extra

    def obs(self):
        cells = [(
            self.cell_type(cell),
            self.crystal(cell),
            self.egg(cell),
            cell.ants[0],
            cell.ants[1])
            for cell in self.game.board.cells]
        return np.array(cells, dtype=int)

    def cell_type(self, cell):
        cell_type = -1
        cell_type = 1 if cell.type == CellType.EGG else cell_type
        cell_type = 2 if cell.type == CellType.FOOD else cell_type
        cell_type = 3 if cell.anthill is not None and cell.anthill.index == 0 else cell_type
        cell_type = 4 if cell.anthill is not None and cell.anthill.index == 1 else cell_type
        cell_type = 0 if cell_type == -1 else cell_type
        return cell_type

    def egg(self, cell):
        return cell.richness if cell.type == CellType.EGG else 0

    def crystal(self, cell):
        return cell.richness if cell.type == CellType.FOOD else 0

    def reset(self, **kwargs):
        # Reset state
        self.game = Game(2)
        self.state = self.obs()

        info = self.game.get_global_info_for(self.game.players[0])
        frame = self.game.get_current_frame_info_for(self.game.players[0])
        summary = self.game.game_summary
        extra = {'info': info, 'frame': frame, 'summary': summary }
        return self.state,extra

    def render(self, mode='human'):
        # Implement rendering
        if mode == 'human' and self.renderer is not None:
            fig, ax = plt.subplots(figsize=(1024 / 100, 768 / 100), dpi=150)
            self.renderer.plot_board(ax, self.game.board)
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.show()

    def close(self):
        # Clean up when done
        pass

