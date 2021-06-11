import gym
from gym.spaces import MultiDiscrete

from action import Action, ActionVerb, ActionObject
from game.character import CharacterState
from game.game import Game
from game.player import AgentPlayer
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = MultiDiscrete([len(ActionVerb), len(ActionObject)])

        self.observation_space = MultiDiscrete(8 * [5, 5] + len(ActionVerb) * len(ActionObject) * [2])

        self.can_take_two_gold = None

    def step(self, a):
        action = Action(a)

        is_valid_action, reason = self.is_valid_action(action)
        if not is_valid_action:
            print('Invalid action:', action.verb.name, action.object.name, ',', reason)
            return self.get_state(), -100, False, {}

        if self.game.round.phase == Phase.CHOOSE_CHARACTERS:
            return self.step_choose_characters(action)
        elif self.game.round.phase == Phase.PLAYER_TURNS:
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
               isinstance(self.game.round.murdered_character.player, AgentPlayer)

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
            self.game.round.current_player.take_2_gold()
            self.can_take_two_gold = 0
            reward = 10

        return self.get_state(), reward, False, {}

    def get_state(self):
        state = []

        # Characters
        for c in self.game.characters:
            if self.game.round.phase == Phase.CHOOSE_CHARACTERS:
                if c.state == CharacterState.DECK or c.state == CharacterState.FACE_UP:
                    state.append(c.state.value)
                    state.append(0)
                else:
                    state.append(0)  # Unknown
                    state.append(0)
            else:  # Player turns
                if isinstance(c.player, AgentPlayer):
                    state.append(c.state.value)
                    state.append(c.player.number)
                else:  # TODO Change character state of other players to CHOSEN when already revealed
                    state.append(0)  # Unknown
                    state.append(0)

        # Valid actions
        for verb in range(len(ActionVerb)):
            for object in range(len(ActionObject)):
                if self.is_valid_action(Action([verb, object])):
                    state.append(1)
                else:
                    state.append(0)

        return state

    def is_valid_action(self, action):
        if self.game.round.phase == Phase.CHOOSE_CHARACTERS:
            if action.verb == ActionVerb.CHOOSE:
                if action.object.is_character():
                    if action.object.to_character(self.game).state == CharacterState.DECK:
                        return True, ''
                    else:
                        return False, 'Chosen character is not in deck'
                else:
                    return False, 'Object must be a character in Phase.CHOOSE_CHARACTERS'
            else:
                return False, 'Verb must be CHOOSE in Phase.CHOOSE_CHARACTERS'
        else:  # Player turns
            if action.verb == ActionVerb.END_TURN:
                if action.object == ActionObject.NONE:
                    return True, ''
                else:
                    return False, 'Object must be NONE when ending turn'
            elif action.verb == ActionVerb.TAKE_TWO_GOLD:
                if action.object == ActionObject.NONE:
                    if self.can_take_two_gold:
                        return True, ''
                    else:
                        return False, 'Cannot take 2 gold'
                else:
                    return False, 'Object must be NONE when taking 2 gold'
            else:
                return False, 'Unsupported verb in Phase.PLAYER_TURNS'

    def reset(self):
        self.game = Game(player_count=4)
        self.agent = self.game.players[0]
        self.game.start()
        self.game.round.start()
        self.can_take_two_gold = 0

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.get_state()
