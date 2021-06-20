import gym

from stable_baselines3 import A2C, PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from callback import SaveOnBestTrainingRewardCallback
from env.env import CitadelsEnv
import os

log_dir = "/Users/daniel/repos/CitadelsAI/logs"
os.makedirs(log_dir, exist_ok=True)

env = CitadelsEnv()
env = Monitor(env, log_dir)

callback = SaveOnBestTrainingRewardCallback(check_freq=100, log_dir=log_dir)

# # Learn
# model = A2C('MlpPolicy', env, verbose=1)
model = PPO('MlpPolicy', env, verbose=1)
model = PPO.load("/Users/daniel/repos/CitadelsAI/logs/best_model.zip", env=env)
model.learn(total_timesteps=100000, callback=callback)

# mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
# print(f"mean_reward:{mean_reward:.2f} +/- {std_reward:.2f}")

# Play
# print('-Play-')
# obs = env.reset()
# for i in range(100):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     # env.render()
#     if done:
#         obs = env.reset()
