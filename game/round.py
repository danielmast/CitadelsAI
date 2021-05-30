import random
from enum import Enum

from game import character
from game.player import Player, face_up_count, AgentPlayer
from game.character import CharacterState


class Round:
    def __init__(self, game, number, crown_player):
        self.game = game
        self.number = number
        self.crown_player = crown_player
        self.current_player = crown_player
        self.character_state = create_character_state()
        self.murdered_character = None
        self.robbed_character = None

    def start_auto(self):
        print('Start round', self.number)

        print(self.crown_player.name, 'has the crown')

        print('Put 1 character face down:')
        face_down = random.choice(self.get_deck_characters())
        self.set_character_state(face_down, CharacterState.FACE_DOWN)
        print(face_down.name())

        print('Face up characters:')
        for i in range(face_up_count(self.game.player_count)):
            face_up = random.choice(self.get_deck_characters())
            self.set_character_state(face_up, CharacterState.FACE_UP)
            print(face_up.name())

        self.choose_characters()
        self.player_turns()

    def start(self):
        print('Start round', self.number)

        print(self.crown_player.name, 'has the crown')

        print('Put 1 character face down:')
        face_down = random.choice(self.get_deck_characters())
        self.set_character_state(face_down, CharacterState.FACE_DOWN)
        print(face_down.name())

        print('Face up characters:')
        for i in range(face_up_count(self.game.player_count)):
            face_up = random.choice(self.get_deck_characters())
            self.set_character_state(face_up, CharacterState.FACE_UP)
            print(face_up.name())

    def choose_characters(self, until_agent_is_up=False):
        while self.current_player is not None:
            if until_agent_is_up and isinstance(self.current_player, AgentPlayer):
                return

            c = self.current_player.choose_character(self.game, self)
            print(self.current_player.name, 'chooses', c.name())
            self.set_character_state(c, self.current_player)
            self.next_player()

    def choose_character(self, player, c):
        if player != self.current_player:
            raise Exception('Player choosing character is not current player')
        if self.get_character_state(c) != CharacterState.DECK:
            raise Exception('Player cannot choose character that is not in deck')

        print(self.current_player.name, 'chooses', c.name())
        self.set_character_state(c, self.current_player)
        self.next_player()

    def next_player(self):
        current_index = self.game.players.index(self.current_player)
        next_player = self.game.players[(current_index + 1) % len(self.game.players)]
        if next_player == self.crown_player:
            self.current_player = None
        else:
            self.current_player = next_player

    def player_turns(self, until_agent_is_up=False):
        for c, state in self.character_state.items():
            if isinstance(state, Player):
                self.current_player = state

                if c.name() == 'King':
                    self.game.next_crown_player = self.current_player

                if self.murdered_character == c:
                    print(self.current_player.name, 'skips a round because his character (', c.name(), ') was murdered')
                    continue

                if self.robbed_character == c:
                    print(self.current_player.name, 'was robbed and loses his gold')
                    self.get_player_by_character('Thief').gold += self.current_player.gold
                    self.current_player.gold = 0

                print(self.current_player.name, 'plays')

                if until_agent_is_up and isinstance(self.current_player, AgentPlayer):
                    return

                self.current_player.play_turn(self.game, self, c)
                self.end_player_turn()

    def end_player_turn(self):
        if len(self.current_player.city) >= 8 and self.game.first_finished_player is None:
            self.game.first_finished_player = self.current_player

    def get_character_state(self, character):
        key = None
        for c in self.character_state.keys():
            if c.name() == character.name():
                key = c
        return self.character_state[key]

    def set_character_state(self, character, state):
        key = None
        for c in self.character_state.keys():
            if c.name() == character.name():
                key = c
        self.character_state[key] = state

    def get_deck_characters(self):
        deck = []
        for c, state in self.character_state.items():
            if state == CharacterState.DECK:
                deck.append(c)
        return deck

    def get_player_by_character(self, character_name):
        for c, state in self.character_state.items():
            if c.name() == character_name:
                return state


class Step(Enum):
    CHOOSE_CHARACTERS = 1
    PLAYER_TURNS = 2


def create_character_state():
    return {
        character.Assassin(): CharacterState.DECK,
        character.Thief(): CharacterState.DECK,
        character.Magician(): CharacterState.DECK,
        character.King(): CharacterState.DECK,
        character.Bishop(): CharacterState.DECK,
        character.Merchant(): CharacterState.DECK,
        character.Architect(): CharacterState.DECK,
        character.Warlord(): CharacterState.DECK
    }
