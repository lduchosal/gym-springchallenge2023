from gymnasium.envs.registration import register

register(
    id="springchallenge2023/AntLeague-v0",
    entry_point="springchallenge2023.envs.ant_league:AntLeagueEnv",
    max_episode_steps=100,
)
register(
    id="springchallenge2023/PyLeague-v0",
    entry_point="springchallenge2023.envs.py_league:PyLeagueEnv",
    max_episode_steps=100,
)

print("springchallenge2023 imported")