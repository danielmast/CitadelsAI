import gym

from action import Action
from game.character import Assassin, Thief, Magician, King, Bishop, Merchant, Architect, Warlord
from game.game import Game
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Discrete(2)

    def step(self, a):
        action = Action(a)

        if not self.is_valid_action(action):
            return self.phase, -100, False, {}

        if self.phase == Phase.CHOOSE_CHARACTERS:
            return self.step_choose_characters(action)
        elif self.phase == Phase.PLAYER_TURNS:
            return self.step_player_turns(action)

    def step_choose_characters(self, action):
        character = None
        if action == Action.CHOOSE_ASSASSIN:
            character = Assassin()
        if action == Action.CHOOSE_THIEF:
            character = Thief()
        if action == Action.CHOOSE_MAGICIAN:
            character = Magician()
        if action == Action.CHOOSE_KING:
            character = King()
        if action == Action.CHOOSE_BISHOP:
            character = Bishop()
        if action == Action.CHOOSE_MERCHANT:
            character = Merchant()
        if action == Action.CHOOSE_ARCHITECT:
            character = Architect()
        if action == Action.CHOOSE_WARLORD:
            character = Warlord()

        self.game.round.choose_character(self.agent, character)
        self.game.round.choose_characters()

        self.phase = Phase.PLAYER_TURNS

        self.game.round.player_turns(until_agent_is_up=True)

        return self.phase, 10, False, {}

    def step_player_turns(self, action):
        if action == Action.TAKE_TWO_GOLD:
            self.game.round.current_player.take_2_gold()

        self.game.round.end_player_turn()
        self.game.round.player_turns()

        if self.game.end_of_game():
            self.game.end()
            return self.phase, 10, True, {}

        self.game.set_next_round()
        self.game.round.start()
        self.phase = Phase.CHOOSE_CHARACTERS

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.phase, 10, False, {}

    def is_valid_action(self, action):
        return True

    def reset(self):
        self.game = Game(player_count=4)
        self.agent = self.game.players[0]
        self.game.start()
        self.game.round.start()
        self.phase = Phase.CHOOSE_CHARACTERS

        self.game.round.choose_characters(until_agent_is_up=True)

        return Phase.CHOOSE_CHARACTERS.value
