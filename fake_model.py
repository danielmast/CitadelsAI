import random

from action import Action
from phase import Phase


class FakeModel:
    def __init__(self, env):
        self.env = env

    def learn(self, total_timesteps):
        for i in range(total_timesteps):
            obs = self.env.reset()
            done = False
            while not done:
                action = self.predict(obs)
                obs, reward, done, info = self.env.step(action)

    def predict(self, obs):
        phase = Phase(obs)
        if phase == Phase.CHOOSE_CHARACTERS:
            return self.predict_choose_character()
        elif phase == Phase.PLAYER_TURNS:
            return self.predict_player_turn()

    def predict_choose_character(self):
        c = self.choose_character(self.env.game)

        if c.name() == 'Assassin':
            action = Action.CHOOSE_ASSASSIN
        elif c.name() == 'Thief':
            action = Action.CHOOSE_THIEF
        elif c.name() == 'Magician':
            action = Action.CHOOSE_MAGICIAN
        elif c.name() == 'King':
            action = Action.CHOOSE_KING
        elif c.name() == 'Bishop':
            action = Action.CHOOSE_BISHOP
        elif c.name() == 'Merchant':
            action = Action.CHOOSE_MERCHANT
        elif c.name() == 'Architect':
            action = Action.CHOOSE_ARCHITECT
        elif c.name() == 'Warlord':
            action = Action.CHOOSE_WARLORD

        return action.value

    def predict_player_turn(self):
        return Action.TAKE_TWO_GOLD.value

    def choose_character(self, game):
        return random.choice(game.round.get_deck_characters())
