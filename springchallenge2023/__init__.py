from gymnasium.envs.registration import register

register(
    id="springchallenge2023/AntLeague-v0",
    entry_point="springchallenge2023.envs.ant_league:AntLeagueEnv",
    max_episode_steps=100,
)
