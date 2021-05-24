import numpy as np
import gym
import random


class CitadelsEnv(gym.Env):

    def __init__(self):
        # There are two actions, first will get reward of 1, second reward of -1.
        self.action_space = gym.spaces.Discrete(5)
        # self.action_space = 1
        self.observation_space = gym.spaces.Discrete(2)

    def step(self, action):

        # if we took an action, we were in state 1
        state = 1

        if action == 2:
            reward = 1
        else:
            reward = -1

        # regardless of the action, game is done after a single step
        done = True

        info = {}

        return state, reward, done, info

    def reset(self):
        state = 0
        return state
