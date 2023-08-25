import gymnasium as gym
import numpy as np
import sys
from springchallenge2023.wrappers.ComputeEggCrystalRatio import ComputeEggCrystalRatio
from springchallenge2023.wrappers.EncodeCellType import EncodeCellType
from springchallenge2023.wrappers.Normalize import Normalize
sys.path.append('../')

from springchallenge2023.wrappers.BeaconAction import BeaconAction
from gymnasium import envs
from gymnasium.wrappers import FlattenObservation
import logging
import threading

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s - %(message)s')
threading.current_thread().name = f'main'

logging.debug(envs.registry.keys())
logging.debug(gym.__version__)

env = gym.make("springchallenge2023/AntLeague-v0")
env = EncodeCellType(env)
env = ComputeEggCrystalRatio(env)
env = Normalize(env)
env = FlattenObservation(env)
env = BeaconAction(env)

np.set_printoptions(precision=1, suppress=True)

#env = AntLeagueEnv()
logging.info("starting")

while True:

    obs, info = env.reset(seed=10)
    logging.info(obs.shape)
    logging.info(obs)

    action = np.random.randint(0, 100, (31,))

    done = False
    while not done:
        action = np.random.randint(0, 100, (31,))
        (obs, reward, terminated, truncated, info) = env.step(action)
        done = terminated or truncated
        logging.debug(obs)
        logging.info(f'reward : {reward}')
        logging.debug(f'done : {done}')

    logging.info(obs)
    logging.info("terminated")

    print("Press Enter to start next game...")
    input()

env.close()


#env = gym.make("springchallenge2023/AntLeague-v0", render_mode=None)
# env.reset()
# 
# print("Observation space:", env.observation_space)
# print("Action space:", env.action_space)
