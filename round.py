from enum import Enum

import character
import player


class Round:
    def __init__(self, game, number, crown_player):
        self.game = game
        self.number = number
        self.crown_player = crown_player
        self.current_player = crown_player
        self.character_deck = character.create_character_deck()
        self.face_up_characters = []
        self.chosen_characters = {}
        self.murdered_character = None
        self.robbed_character = None
        self.step = Step.CHOOSE_CHARACTERS

    def start(self):
        print('Start round', self.number)

        print('Put one character face down')
        self.character_deck.pop()
        for i in range(player.face_up_count(self.game.player_count)):
            self.face_up_characters.append(self.character_deck.pop())
        print('Face up characters:')
        for c in self.face_up_characters:
            print(c.name())

        while self.current_player is not None:
            c = self.current_player.choose_character(self.game, self)
            self.chosen_characters[self.crown_player.name] = c
            self.next_player()

        self.step = Step.PLAYER_TURNS
        # todo Player turns

    def next_player(self):
        if self.step == Step.CHOOSE_CHARACTERS:
            current_index = self.game.players.index(self.current_player)
            next_player = self.game.players[(current_index + 1) % len(self.game.players)]
            if next_player == self.crown_player:
                self.current_player = None
            else:
                self.current_player = next_player
        elif self.step == Step.PLAYER_TURNS:
            pass  # todo player turns


class Step(Enum):
    CHOOSE_CHARACTERS = 1
    PLAYER_TURNS = 2
