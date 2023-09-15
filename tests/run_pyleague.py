import gymnasium as gym
import numpy as np
import sys
sys.path.append('../')

from gymnasium import envs

import logging
import threading
import springchallenge2023

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s - %(message)s')
threading.current_thread().name = f'main'

logging.debug(envs.registry.keys())
logging.debug(gym.__version__)


def make_env():

    env = gym.make("springchallenge2023/PyLeague-v0", render_mode='human')
    return env

np.set_printoptions(precision=1, suppress=True)

logging.info("starting")

env = make_env()

while True:

    state, info = env.reset()
    logging.info(state.shape)
    logging.info(state)

    done = False
    while not done:
        env.render()  # Set the render_mode here
        action = np.random.randint(0, 300, (15,))
        (state, reward, terminated, truncated, info) = env.step(action)
        done = terminated or truncated
        logging.debug(state)
        logging.info(f'reward : {reward}')
        logging.debug(f'done : {done}')

    logging.info(state)
    logging.info("terminated")

    print("Press Enter to start next game...")
    input()

env.close()

