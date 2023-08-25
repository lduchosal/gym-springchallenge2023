import numpy as np
from gymnasium import ObservationWrapper, spaces


class Normalize(ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = spaces.Dict({
            'map': spaces.Box(
                low=np.zeros((31, 11), dtype=float),
                high=np.full((31, 11), 1, dtype=float),
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
        cols_to_normalize = obs['map'][:, 4:10]

        # Calculate min and max for these columns
        min_values = np.min(cols_to_normalize, axis=0)
        max_values = np.max(cols_to_normalize, axis=0)

        # Normalize the columns using min-max normalization
        epsilon = 1e-10
        normalized_cols = (cols_to_normalize - min_values) / (max_values - min_values + epsilon)

        # logging.debug(f"before obs {obs}")
        obs['map'][:, 4:10] = normalized_cols
        # logging.debug(f"after obs {obs}")

        return obs