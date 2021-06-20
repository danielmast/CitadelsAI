import gym
from gym.spaces import MultiDiscrete, Discrete

from action import Action, ActionVerb, ActionObject
from game.character import CharacterState
from game.game import Game
from game.player import AgentPlayer
from phase import Phase


class CitadelsEnv(gym.Env):

    def __init__(self):
        self.action_space = Discrete(232)

        self.observation_space = MultiDiscrete(8 * [5, 5] + 232 * [2])

        self.can_take_two_gold = None
        self.can_draw_two_districts = None
        self.must_discard_district = None
        self.can_build = None

    def step(self, a):
        action = Action(a)

        is_valid_action, reason = action.is_valid(self)
        if not is_valid_action:
            print('Invalid action:', action.verb.name, action.object.name, ',', reason)
            return self.get_state(), 0, False, {}

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
            self.can_take_two_gold = True
            self.can_draw_two_districts = True
            self.must_discard_district = False
            self.can_build = False

        return self.get_state(), 0, False, {}

    def agent_is_murdered(self):
        return self.game.round.murdered_character is not None and \
               isinstance(self.game.round.murdered_character.player, AgentPlayer)

    def step_player_turns(self, action):
        reward = 0
        if action.verb == ActionVerb.END_TURN:
            if self.can_take_two_gold or self.can_draw_two_districts:
                reward = reward - 2
            if self.can_build and self.game.round.current_player.gold > 10:
                reward = reward - 2
            self.game.round.end_player_turn()
            self.game.round.player_turns(continued=True)

            if self.game.end_of_game():
                self.game.end()
                return self.get_state(), reward, True, {}

            self.game.set_next_round()
            self.game.round.start()

            self.game.round.choose_characters(until_agent_is_up=True)
        elif action.verb == ActionVerb.TAKE_TWO_GOLD:
            if self.game.round.current_player.gold > 10:
                reward = reward - 2
            self.game.round.current_player.take_2_gold()
            self.can_take_two_gold = False
            self.can_draw_two_districts = False
            self.can_build = True
        elif action.verb == ActionVerb.DRAW_TWO_DISTRICTS:
            if len(self.game.round.current_player.hand()) > 8:
                reward = reward - 2
            self.game.round.current_player.draw_district(self.game)
            self.game.round.current_player.draw_district(self.game)
            self.can_take_two_gold = False
            self.can_draw_two_districts = False
            self.must_discard_district = True
        elif action.verb == ActionVerb.DISCARD:
            self.game.round.current_player.discard_district(
                self.game, action.object.to_district(self.game))
            self.game.round.current_player.put_drawn_districts_in_hand()
            self.must_discard_district = False
            self.can_build = True
        elif action.verb == ActionVerb.BUILD:
            district = action.object.to_district(self.game)
            self.game.round.current_player.build_district(district)
            self.can_build = False
            reward = district.value

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
        for a in range(232):
            if Action(a).is_valid(self):
                state.append(1)
            else:
                state.append(0)

        return state

    def reset(self):
        self.game = Game(player_count=4)
        self.agent = self.game.players[0]
        self.game.start()
        self.game.round.start()

        self.game.round.choose_characters(until_agent_is_up=True)

        return self.get_state()
