import numpy as np
from gymnasium import ObservationWrapper, spaces


class ComputeEggCrystalRatio(ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)
        self.observation_space = spaces.Dict({
            'map': spaces.Box(
                low=np.zeros((15, 13), dtype=float),
                high=np.full((15, 13), 300, dtype=float),
                dtype=float),
            'ratio_crystal': spaces.Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=float),
            'ratio_oppants': spaces.Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=float)
        })


    def observation(self, obs):

        sum_crystal = np.sum(obs[:, 4])
        sum_egg = np.sum(obs[:, 5])
        sum_myants = np.sum(obs[:, 6])
        sum_oppants = np.sum(obs[:, 7])


        ratio_crystal_to_myants = 1 / (sum_crystal / sum_myants)
        # ratio_eggs_to_myants = 1 / (sum_egg / sum_myants)
        ratio_oppants_to_myants = 1 / (sum_oppants / sum_myants)


        return {
            'map': obs,
            'ratio_crystal': ratio_crystal_to_myants,
            'ratio_oppants': ratio_oppants_to_myants
            }