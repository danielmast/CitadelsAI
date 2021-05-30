import gym

from stable_baselines3 import A2C

from env.env import CitadelsEnv
from fake_model import FakeModel

env = CitadelsEnv()

fake_model = FakeModel(env)
fake_model.learn(total_timesteps=1000)

# # Learn
# model = A2C('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps=1000)
#
# # Play
# obs = env.reset()
# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     # env.render()
#     if done:
#       obs = env.reset()