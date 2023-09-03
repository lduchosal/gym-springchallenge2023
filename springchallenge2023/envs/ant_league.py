from posixpath import expanduser
from gymnasium import Env, spaces

import numpy as np

import queue
import subprocess
import pygame

import threading
import socketserver
import logging

import re


class AntLeagueEnv(Env):

    metadata = {"render_modes": ["human"], "render_fps": 4}

    _obs = queue.Queue()
    _info = queue.Queue()
    _action = queue.Queue()
    _reward = queue.Queue()
    _terminated = queue.Queue()
    _seed = None
    _player = None

    def __init__(self, render_mode=None):

        print("AntLeagueEnv __init__")

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

        # Start player agent
        HOST, PORT = "localhost", 6666
        player = ThreadedLeagueServer((HOST, PORT), TcpPlayerHandler)
        player.obs = self._obs
        player.info = self._info
        player.action = self._action
        player.reward = self._reward
        player.terminated = self._terminated
        player.__enter__()
        
        self._player = player

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self._seed = seed
        logging.debug(f"seed: {seed}")

        # Start player agent    
        player_thread = threading.Thread(
            target=self._player.serve_forever,
            name='player'
        )
        player_thread.daemon = True
        player_thread.start()

        # Start the command in a separate thread
        referee = threading.Thread(
            target=self._run_antserver,
            name='referee'
            )
        referee.daemon = True
        referee.start()

        self._terminated.queue.clear()

        if self.render_mode == "human":
            self._render_frame()

        logging.debug("waiting for obs")
        obs = self._obs.get()
        info = self._info.get()

        return obs, info

    def step(self, action):

        self._action.put(action)

        logging.debug(f"Waiting for obs")
        observation = self._obs.get()
        logging.debug(f"observation: {observation}")

        logging.debug(f"Waiting for info")
        info = self._info.get()
        logging.debug(f"info: {info}")

        terminated = not self._terminated.empty()
        logging.debug(f"Waiting for reward")
        reward = self._reward.get()
        logging.debug(f"reward: {reward}")
        truncated = False

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info

    def render(self):
        return ""
    
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

        self._player.shutdown()
        self._player.__exit__()


    # Define the function that runs the command
    def _run_antserver(self):

        logging.info("_run_antserver START")
        # Define the working directory and the command
        cwd = '~/Projects/SpringChallenge2023/'
        cmd = [
            '/opt/homebrew/Cellar/openjdk@11/11.0.20/bin/java',
            '--illegal-access=permit',
            '-cp',
            'target/spring-2023-ants-1.0-SNAPSHOT-jar-with-dependencies.jar:target/test-classes',
            'AntLeagueMain'
        ]

        if self._seed != None:
            cmd.extend(str(self._seed))

        # Expand the user's home directory
        cwd = expanduser(cwd)
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print the output of the command
        stdout, stderr = process.communicate()
        logging.debug(f"STDOUT: {stdout}")
        logging.debug(f"STDERR: {stderr}")

        pattern = r'"scores":\{"0":(-?\d+),"1":(-?\d+)\}'
        match = re.search(pattern, stdout)

        reward = -10
        if match:

            score0 = int(match.group(1))
            score1 = int(match.group(2))

            if score0 < 0: # illegal move
                reward = -10000
            else:
                reward = ((score0 - score1) / (score0 + score1)) * 1000

        self._reward.put(reward)
        self._terminated.put("terminated")

        # if reward > 0:
        f = open("ant_league.txt", "a")
        f.write(stdout)
        f.close()

        process.wait()
        process.terminate()
        logging.info("_run_antserver STOP")



class ThreadedLeagueServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def process_request_thread(self, request, client_address):
        threading.current_thread().name = f'player'
        super().process_request_thread(request, client_address)


class TcpPlayerHandler(socketserver.StreamRequestHandler):

    def finish(self) -> None:
        logging.debug("TcpPlayerHandler finish")
        return super().finish()
    
    def setup(self):

        super().setup()  # Call the parent class's setup method
        # self.connection.settimeout(1.0)  # Set a timeout of 5 seconds
        logging.debug("TcpPlayerHandler setup")


    def handle(self):
        logging.debug("TcpPlayerHandler START")
        logging.debug("{} wrote:".format(self.client_address[0]))

        info = {}
        line = self.rfile.readline() # cells

        cells = int(line)
        obs = np.zeros((cells, 5), dtype=int) # celltype, eggs, crystal, myants, oppants

        for i in range(cells):
            line = self.rfile.readline() # celltype, resource, neigh0 .. neigh5            
            celltype, resource, n0, n1, n2, n3, n4, n5 = [int(sd) for sd in line.split()]
            obs[i][0] = celltype # 0 = none, 1 = egg, 2 = crystal, 3 = mybase, 4 = oppbase
            obs[i][celltype-1] = resource

        line = self.rfile.readline() # bases
        bases = int(line)

        line = self.rfile.readline() # mybase
        mybases = [int(i) for i in line.split()]
        for i in range(bases):
            obs[mybases[i]][0] = 3 # mybases
        
        line = self.rfile.readline() # oppbase
        oppbases = [int(i) for i in line.split()]
        for i in range(bases):
            obs[oppbases[i]][0] = 4 # oppbases

        reward = None

        score = 0
        # game
        while True:

            line = self.rfile.readline() # scores
            sdata = line.split()
            if len(sdata) == 0: # end of game
                self.server.obs.put(obs)
                self.server.info.put(info)
                self.server.terminated.put("terminated")
                logging.debug(f"end of game")
                logging.debug("TcpPlayerHandler STOP")
                return

            myscore, oppscore = [int(i) for i in sdata]

            for i in range(cells):
                line = self.rfile.readline() # reource, myant, oppant
                # logging.debug(f"line: {line}")
                (resource, myant, oppant) = [int(sd) for sd in line.split()]

                celltype = int(obs[i][0])
                obs[i][celltype-1] = resource #  eggs or crystal
                obs[i][3] = myant #  myants, 
                obs[i][4] = oppant #  oppants

            self.server.obs.put(obs)
            self.server.info.put(info)

            if reward != None:
                self.server.reward.put(reward)

            info = {}

            # logging.debug("waiting for action")
            action = self.server.action.get()
            reward = myscore - score
            score = myscore
            # logging.debug(f"got action {action}")

            # Likewise, self.wfile is a file-like object used to write back
            # to the client
            self.wfile.write(bytes("{}".format(action), "ascii"))
            self.wfile.write(bytes("\n", "ascii"))

        logging.debug("TcpPlayerHandler STOP")
