import gym
from gym.spaces import MultiDiscrete

from action import Action, ActionVerb, ActionObject
from game.character import Assassin, Thief, Magician, King, Bishop, Merchant, Architect, Warlord, CharacterState
from game.game import Game
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = MultiDiscrete([len(ActionVerb), len(ActionObject)])
        self.observation_space = MultiDiscrete([2] + (8 * [2]))

    def step(self, a):
        action = Action(a)

        if self.phase == Phase.CHOOSE_CHARACTERS:
            if action.verb != ActionVerb.CHOOSE or not action.object.is_character():
                print('Invalid action: Agent did not choose a character:', a)
                return self.get_state(), -100, False, {}
            return self.step_choose_characters(action)
        elif self.phase == Phase.PLAYER_TURNS:
            if (action.verb != ActionVerb.TAKE_TWO_GOLD and action.verb != ActionVerb.END_TURN) \
                    or action.object != ActionObject.NONE:
                print('Invalid action: Agent did not do a (currently supported) player turn action, ', a)
                return self.get_state(), -100, False, {}
            return self.step_player_turns(action)

    def step_choose_characters(self, action):
        character = None
        if action.object == ActionObject.ASSASSIN:
            character = Assassin()
        elif action.object == ActionObject.THIEF:
            character = Thief()
        elif action.object == ActionObject.MAGICIAN:
            character = Magician()
        elif action.object == ActionObject.KING:
            character = King()
        elif action.object == ActionObject.BISHOP:
            character = Bishop()
        elif action.object == ActionObject.MERCHANT:
            character = Merchant()
        elif action.object == ActionObject.ARCHITECT:
            character = Architect()
        elif action.object == ActionObject.WARLORD:
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
        if action.verb == ActionVerb.END_TURN:
            self.game.round.end_player_turn()
            self.game.round.player_turns(continued=True)

            if self.game.end_of_game():
                self.game.end()
                return self.get_state(), reward, True, {}

            self.game.set_next_round()
            self.game.round.start()
            self.phase = Phase.CHOOSE_CHARACTERS

            self.game.round.choose_characters(until_agent_is_up=True)
        elif action.verb == ActionVerb.TAKE_TWO_GOLD:
            self.game.round.current_player.take_2_gold()
            reward = 10

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
