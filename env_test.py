import gym

from stable_baselines3 import A2C, PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import SubprocVecEnv

from env.env import CitadelsEnv
from fake_model import FakeModel

def make_env(rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """

    def _init():
        env = CitadelsEnv()
        env.seed(seed + rank)
        return env

    set_random_seed(seed)
    return _init


if __name__ == '__main__':
    # env = CitadelsEnv()
    env = SubprocVecEnv([make_env(i) for i in range(8)])

    # fake_model = FakeModel(env)
    # fake_model.learn(total_timesteps=1000)

    # # Learn
    # model = A2C('MlpPolicy', env, verbose=1)
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=100000)

    # # Play
    obs = env.reset()
    print('Let\'s play')
    for i in range(100000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        # env.render()
        if done:
            obs = env.reset()


