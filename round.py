import random
from enum import Enum

import character
from player import Player, face_up_count
from character import CharacterState


class Round:
    def __init__(self, game, number, crown_player):
        self.game = game
        self.number = number
        self.crown_player = crown_player
        self.current_player = crown_player
        self.character_state = create_character_state()
        self.murdered_character = None
        self.robbed_character = None

    def start(self):
        print('Start round', self.number)

        print('Put one character face down:')
        face_down = random.choice(self.get_deck_characters())
        self.character_state[face_down] = CharacterState.FACE_DOWN
        print(face_down.name())

        print('Face up characters:')
        for i in range(face_up_count(self.game.player_count)):
            face_up = random.choice(self.get_deck_characters())
            self.character_state[face_up] = CharacterState.FACE_UP
            print(face_up.name())

        while self.current_player is not None:
            c = self.current_player.choose_character(self.game, self)
            print(self.current_player.name, 'chooses', c.name())
            self.character_state[c] = self.current_player
            self.next_player()

        for c, state in self.character_state.items():
            if isinstance(state, Player):
                self.current_player = state
                print(self.current_player.name, 'plays')
                self.current_player.play_turn(self.game, self)

    def next_player(self):
        current_index = self.game.players.index(self.current_player)
        next_player = self.game.players[(current_index + 1) % len(self.game.players)]
        if next_player == self.crown_player:
            self.current_player = None
        else:
            self.current_player = next_player

    def get_deck_characters(self):
        deck = []
        for c, state in self.character_state.items():
            if state == CharacterState.DECK:
                deck.append(c)
        return deck


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
