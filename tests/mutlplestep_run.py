import gymnasium as gym
import numpy as np
import sys
from springchallenge2023.wrappers.BeaconAction import BeaconAction
from springchallenge2023.wrappers.ComputeEggCrystalRatio import ComputeEggCrystalRatio
from springchallenge2023.wrappers.EncodeCellType import EncodeCellType
from springchallenge2023.wrappers.Normalize import Normalize
sys.path.append('../')

from springchallenge2023.wrappers.MultipleStepWrapper import MultipleStepWrapper
from gymnasium import envs
from gymnasium.wrappers import FlattenObservation
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(threadName)s - %(message)s')
threading.current_thread().name = f'main'

logging.debug(envs.registry.keys())
logging.debug(gym.__version__)

env = gym.make("springchallenge2023/AntLeague-v0") # obs (15, 5)  int,   action str
env = BeaconAction(env)                            # obs (15, 5)  int,   action (15,) float
env = MultipleStepWrapper(env)                     # obs (15, 7)  int,   action (1,) float
env = EncodeCellType(env)                          # obs (15, 11) int,   action (15,)
env = ComputeEggCrystalRatio(env)                  # { map = obs (15, 13) float, ratio = float }, action (15,)
env = Normalize(env)                               # { map = obs (15, 13) float, ratio = float }, action (15,)
env = FlattenObservation(env)                      # obs (167, ) float, action (15,)

np.set_printoptions(precision=1, suppress=True)

#env = AntLeagueEnv()
logging.info("starting")


obs, info = env.reset(seed=10)
logging.info(obs.shape)
logging.info(obs)

action = np.random.randint(0, 300)

done = False
while not done:
    action = np.random.randint(0, 300)
    (obs, reward, terminated, truncated, info) = env.step(action)
    done = terminated or truncated
    logging.debug(obs)
    logging.info(f'reward : {reward}')
    logging.debug(f'done : {done}')

logging.info(obs)
logging.info("terminated")

env.close()


#env = gym.make("springchallenge2023/AntLeague-v0", render_mode=None)
# env.reset()
# 
# print("Observation space:", env.observation_space)
# print("Action space:", env.action_space)
