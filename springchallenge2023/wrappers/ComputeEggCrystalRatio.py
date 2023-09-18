import sys

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

        # celltype, eggs, crystal, myants, oppants
        # (0,1,2,3,4), eggs, crystal, myants, oppants

        sum_crystal = np.sum(obs[:, 4])
        sum_egg = np.sum(obs[:, 5])
        sum_myants = np.sum(obs[:, 6])
        sum_oppants = np.sum(obs[:, 7])
        epsilon = sys.float_info.epsilon

        ratio_crystal_to_myants = 1 / ((sum_crystal+ epsilon) / sum_myants)
        ratio_eggs_to_myants = 1 / ((sum_egg+ epsilon) / sum_myants)
        ratio_oppants_to_myants = 1 / ((sum_oppants+ epsilon) / sum_myants)


        return {
            'map': obs,
            # 'sum_crystal': sum_crystal,
            # 'sum_egg': sum_egg,
            # 'sum_myants': sum_myants,
            # 'sum_oppants': sum_oppants,
            'ratio_crystal': ratio_crystal_to_myants,
            # 'ratio_eggs_to_myants': ratio_eggs_to_myants,
            'ratio_oppants': ratio_oppants_to_myants
            }