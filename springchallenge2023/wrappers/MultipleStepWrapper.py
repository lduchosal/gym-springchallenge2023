import numpy as np
from gymnasium import Wrapper, spaces


import logging
from typing import Optional


class MultipleStepWrapper(Wrapper):


    def __init__(self, env):

        super().__init__(env)

        self.observation_space = spaces.Box(
            low=np.zeros((31, 7), dtype=int),
            high=np.full((31, 7), 300, dtype=int),
            dtype=int)

        self.action_space = list(range(300))

    def reset(
        self, seed: Optional[int] = None, options: Optional[dict] = None
    ):
        """Resets the environment.

        Args:
            seed: the seed to reset the environment with
            options: the options to reset the environment with

        Returns:
            (observation, info)
        """

        obs, info = self.env.reset(seed=seed)

        self.stepcounter = 0
        self.lastobs = obs
        self.lastinfo = info
        self.lastreward = -1

        self.beacons = np.zeros((obs.shape[0], 1), dtype=int)
        currentstep = self.one_hot_encode(self.stepcounter)
        obs = np.hstack((obs, self.beacons))
        obs = np.hstack((obs, currentstep))

        return obs, info


    def one_hot_encode(self, num):
        num = num % 31
        encoded = np.zeros((31,1))
        encoded[num] = 1
        return encoded


    def step(self, action):

        if self.stepcounter >= 31:

            act = self.beacons.squeeze().astype(int)
            obs, reward, terminated, truncated, info = self.env.step(act)
            self.lastobs = obs
            self.lastinfo = info
            self.lastreward = reward
            self.stepcounter = 0

            # self.beacons = np.zeros((obs.shape[0], 1))
            currentstep = self.one_hot_encode(self.stepcounter)
            obs = np.hstack((obs, self.beacons))
            obs = np.hstack((obs, currentstep))

            return obs, reward, terminated, truncated, info

        self.beacons[self.stepcounter] = action
        obs = self.lastobs

        self.stepcounter = self.stepcounter + 1
        currentstep = self.one_hot_encode(self.stepcounter)
        obs = np.hstack((obs, self.beacons))
        obs = np.hstack((obs, currentstep))


        reward = self.lastreward
        info = self.lastinfo
        terminated = False
        truncated = False

        logging.debug(f'obs : {obs}')

        return obs, reward, terminated, truncated, info