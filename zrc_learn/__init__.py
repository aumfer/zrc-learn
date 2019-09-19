from gym.envs.registration import register

register(
    id='zrc-v0',
    entry_point='zrc_learn.envs:ZrcEnv',
)
