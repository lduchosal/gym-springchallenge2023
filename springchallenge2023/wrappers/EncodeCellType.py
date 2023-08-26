import numpy as np
from gymnasium import ObservationWrapper, spaces
from sklearn.preprocessing import OneHotEncoder


class EncodeCellType(ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)
        self.observation_space = spaces.Box(
            low=np.zeros((15, 11), dtype=int),
            high=np.full((15, 11), 100, dtype=int),
            dtype=float)

    def observation(self, obs):
        celltype = obs[:, 0].reshape(-1, 1)
        encoder = OneHotEncoder(sparse_output=False, categories='auto')
        encoded_celltype = encoder.fit_transform(celltype)

        obs = obs[:, 1:]
        obs = np.hstack((encoded_celltype, obs))
        return obs