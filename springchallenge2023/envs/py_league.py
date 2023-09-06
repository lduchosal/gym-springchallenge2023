import gymnasium as gym
import numpy as np
from gymnasium import spaces


class PyLeagueEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super(PyLeagueEnv, self).__init__()

        print("PyLeagueEnv __init__")

        # Define action and observation space
        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(
            low=np.zeros((15, 5), dtype=int),
            high=np.full((15, 5), 300, dtype=int),
            dtype=int)

        # actions is a string, user actionwrappers
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
        self.reset()

    def step(self, action):
        # Implement your step logic here
        reward = 0
        done = False
        info = {}

        # Update state based on action

        return self.state, reward, done, info

    def reset(self):
        # Reset state
        self.state = self.observation_space.sample()
        return self.state

    def render(self, mode='human'):
        # Implement rendering
        pass

    def close(self):
        # Clean up when done
        pass
