import gym
from gym.spaces import MultiDiscrete

from action import Action, ActionVerb, ActionObject
from game.character import Assassin, Thief, Magician, King, Bishop, Merchant, Architect, Warlord, CharacterState
from game.game import Game
from game.player import AgentPlayer
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = MultiDiscrete([len(ActionVerb), len(ActionObject)])
        self.observation_space = MultiDiscrete([2] + (8 * [2]) + [2])
        self.can_take_two_gold = None

    def step(self, a):
        action = Action(a)

        if self.game.round.phase == Phase.CHOOSE_CHARACTERS:
            if action.verb != ActionVerb.CHOOSE or not action.object.is_character():
                print('Invalid action: Agent did not choose a character:', a)
                return self.get_state(), -100, False, {}
            return self.step_choose_characters(action)
        elif self.game.round.phase == Phase.PLAYER_TURNS:
            if (action.verb != ActionVerb.TAKE_TWO_GOLD and action.verb != ActionVerb.END_TURN) \
                    or action.object != ActionObject.NONE:
                print('Invalid action: Agent did not do a (currently supported) player turn action, ', a)
                return self.get_state(), -100, False, {}
            return self.step_player_turns(action)

    def step_choose_characters(self, action):
        character = None
        if action.object == ActionObject.ASSASSIN:
            character = self.game.get_character('Assassin')
        elif action.object == ActionObject.THIEF:
            character = self.game.get_character('Thief')
        elif action.object == ActionObject.MAGICIAN:
            character = self.game.get_character('Magician')
        elif action.object == ActionObject.KING:
            character = self.game.get_character('King')
        elif action.object == ActionObject.BISHOP:
            character = self.game.get_character('Bishop')
        elif action.object == ActionObject.MERCHANT:
            character = self.game.get_character('Merchant')
        elif action.object == ActionObject.ARCHITECT:
            character = self.game.get_character('Architect')
        elif action.object == ActionObject.WARLORD:
            character = self.game.get_character('Warlord')

        if not self.game.character_state[character] == CharacterState.DECK:
            print('Invalid action: Agent tried to choose character not in deck')
            return self.get_state(), -100, False, {}

        self.game.round.choose_character(self.agent, character)
        self.game.round.choose_characters()

        self.game.round.player_turns(until_agent_is_up=True)

        if self.agent_is_murdered():
            if self.game.end_of_game():
                self.game.end()
                return self.get_state(), 0, True, {}

            self.game.set_next_round()
            self.game.round.start()

            self.game.round.choose_characters(until_agent_is_up=True)
        else:
            self.can_take_two_gold = 1

        return self.get_state(), 0, False, {}

    def agent_is_murdered(self):
        return self.game.round.murdered_character is not None and \
               isinstance(self.game.round.get_player_by_character(self.game.round.murdered_character), AgentPlayer)

    def step_player_turns(self, action):
        reward = 0
        if action.verb == ActionVerb.END_TURN:
            self.game.round.end_player_turn()
            self.game.round.player_turns(continued=True)

            if self.game.end_of_game():
                self.game.end()
                return self.get_state(), reward, True, {}

            self.game.set_next_round()
            self.game.round.start()

            self.game.round.choose_characters(until_agent_is_up=True)
        elif action.verb == ActionVerb.TAKE_TWO_GOLD:
            if self.can_take_two_gold == 1:
                self.game.round.current_player.take_2_gold()
                self.can_take_two_gold = 0
                reward = 10
            else:
                reward = -100
                print('Invalid action: Agent cannot take 2 gold')

        return self.get_state(), reward, False, {}

    def get_state(self):
        state = [self.game.round.phase.value]

        for c, c_state in self.game.character_state.items():
            if self.game.round.phase == Phase.CHOOSE_CHARACTERS and c_state == CharacterState.DECK:
                state.append(1)
            else:
                state.append(0)

        state.append(self.can_take_two_gold)

        return state

    def reset(self):
        self.game = Game(player_count=4)
        self.agent = self.game.players[0]
        self.game.start()
        self.game.round.start()
        self.can_take_two_gold = 0

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.get_state()
