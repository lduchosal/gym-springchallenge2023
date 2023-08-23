import gymnasium as gym
import numpy as np
import sys
sys.path.append('../')

from springchallenge2023.envs.ant_league import EncodeCellType, ComputeEggCrystalRatio, Normalize, BeaconAction
from gymnasium import envs
from gymnasium.wrappers import FlattenObservation
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(threadName)s - %(message)s')
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
env.close()

#env = gym.make("springchallenge2023/AntLeague-v0", render_mode=None)
# env.reset()
# 
# print("Observation space:", env.observation_space)
# print("Action space:", env.action_space)
