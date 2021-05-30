import gym
from gym.spaces import Discrete, MultiDiscrete

from action import Action
from game.character import Assassin, Thief, Magician, King, Bishop, Merchant, Architect, Warlord, CharacterState
from game.game import Game
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = Discrete(len(Action))
        self.observation_space = MultiDiscrete([2] + (8 * [2]))

    def step(self, a):
        action = Action(a)

        if self.phase == Phase.CHOOSE_CHARACTERS:
            if a > 7:
                print('Invalid action: Agent did not choose a character')
                return self.get_state(), -100, False, {}
            return self.step_choose_characters(action)
        elif self.phase == Phase.PLAYER_TURNS:
            if a <= 7:
                print('Invalid action: Agent did not do a player turn action')
                return self.get_state(), -100, False, {}
            return self.step_player_turns(action)

    def step_choose_characters(self, action):
        character = None
        if action == Action.CHOOSE_ASSASSIN:
            character = Assassin()
        elif action == Action.CHOOSE_THIEF:
            character = Thief()
        elif action == Action.CHOOSE_MAGICIAN:
            character = Magician()
        elif action == Action.CHOOSE_KING:
            character = King()
        elif action == Action.CHOOSE_BISHOP:
            character = Bishop()
        elif action == Action.CHOOSE_MERCHANT:
            character = Merchant()
        elif action == Action.CHOOSE_ARCHITECT:
            character = Architect()
        elif action == Action.CHOOSE_WARLORD:
            character = Warlord()

        if not self.game.round.get_character_state(character) == CharacterState.DECK:
            print('Invalid action: Agent tried to choose character not in deck')
            return self.get_state(), -100, False, {}

        self.game.round.choose_character(self.agent, character)
        self.game.round.choose_characters()

        self.phase = Phase.PLAYER_TURNS

        self.game.round.player_turns(until_agent_is_up=True)

        return self.get_state(), 10, False, {}

    def step_player_turns(self, action):
        reward = 0
        if action == Action.DO_NOTHING:
            reward = -5
        elif action == Action.TAKE_TWO_GOLD:
            self.game.round.current_player.take_2_gold()
            reward = 10

        self.game.round.end_player_turn()
        self.game.round.player_turns(continued=True)

        if self.game.end_of_game():
            self.game.end()
            return self.get_state(), reward, True, {}

        self.game.set_next_round()
        self.game.round.start()
        self.phase = Phase.CHOOSE_CHARACTERS

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.get_state(), reward, False, {}

    def get_state(self):
        state = [self.phase.value]

        for c, c_state in self.game.round.character_state.items():
            if self.phase == Phase.CHOOSE_CHARACTERS and c_state == CharacterState.DECK:
                state.append(1)
            else:
                state.append(0)

        return state

    def reset(self):
        self.game = Game(player_count=4)
        self.agent = self.game.players[0]
        self.game.start()
        self.game.round.start()
        self.phase = Phase.CHOOSE_CHARACTERS

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.get_state()
