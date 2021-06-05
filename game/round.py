import random
from enum import Enum

from game.player import Player, face_up_count, AgentPlayer
from game.character import CharacterState, King
from phase import Phase


class Round:
    def __init__(self, game, number, crown_player):
        self.game = game
        self.number = number
        self.phase = Phase.CHOOSE_CHARACTERS
        self.crown_player = crown_player
        self.current_player = crown_player
        self.murdered_character = None
        self.robbed_character = None

    def start_auto(self):
        print('Start round', self.number)

        print(self.crown_player.name, 'has the crown')

        self.deck_characters()

        print('Put 1 character face down:')
        face_down = random.choice(self.get_deck_characters())
        face_down.state = CharacterState.FACE_DOWN
        print(face_down.name())

        print('Face up characters:')
        for i in range(face_up_count(self.game.player_count)):
            face_up = random.choice(self.get_deck_characters())
            face_up.state = CharacterState.FACE_UP
            print(face_up.name())

        self.choose_characters()
        self.player_turns()

    def start(self):
        print('Start round', self.number)

        print(self.crown_player.name, 'has the crown')

        self.deck_characters()

        print('Put 1 character face down:')
        face_down = random.choice(self.get_deck_characters())
        face_down.state = CharacterState.FACE_DOWN
        print(face_down.name())

        print('Face up characters:')
        for i in range(face_up_count(self.game.player_count)):
            face_up = random.choice(self.get_deck_characters())
            face_up.state = CharacterState.FACE_UP
            print(face_up.name())

    def choose_characters(self, until_agent_is_up=False):
        self.phase = Phase.CHOOSE_CHARACTERS
        while self.current_player is not None:
            if until_agent_is_up and isinstance(self.current_player, AgentPlayer):
                return

            c = self.current_player.choose_character(self.game, self)
            print(self.current_player.name, 'chooses', c.name())
            c.choose(self.current_player)
            self.next_player()

    def choose_character(self, player, c):
        if player != self.current_player:
            raise Exception('Player choosing character is not current player')
        if c.state != CharacterState.DECK:
            raise Exception('Player cannot choose character that is not in deck')

        print(self.current_player.name, 'chooses', c.name())
        c.choose(self.current_player)
        self.next_player()

    def next_player(self):
        current_index = self.game.players.index(self.current_player)
        next_player = self.game.players[(current_index + 1) % len(self.game.players)]
        if next_player == self.crown_player:
            self.current_player = None
        else:
            self.current_player = next_player

    def player_turns(self, until_agent_is_up=False, continued=False):
        self.phase = Phase.PLAYER_TURNS
        for c in self.game.characters:
            if continued:
                if self.current_player == c.player:
                    continued = False
                continue

            if c.player is not None:
                self.current_player = c.player

                if isinstance(c, King):
                    self.game.next_crown_player = self.current_player

                if self.murdered_character == c:
                    print(self.current_player.name, 'skips a round because his character (', c.name(), ') was murdered')
                    continue

                if self.robbed_character == c:
                    print(self.current_player.name, 'was robbed and loses his gold')
                    self.game.get_character('Thief').player.gold += self.current_player.gold
                    self.current_player.gold = 0

                print(self.current_player.name, 'plays')

                if until_agent_is_up and isinstance(self.current_player, AgentPlayer):
                    return

                self.current_player.play_turn(self.game, self, c)
                self.end_player_turn()

    def end_player_turn(self):
        print(self.current_player.name, 'ends turn')
        if len(self.current_player.city) >= 8 and self.game.first_finished_player is None:
            self.game.first_finished_player = self.current_player

    def get_deck_characters(self):
        deck = []
        for c in self.game.characters:
            if c.state == CharacterState.DECK:
                deck.append(c)
        return deck

    def deck_characters(self):
        for c in self.game.characters:
            c.deck()


class Step(Enum):
    CHOOSE_CHARACTERS = 1
    PLAYER_TURNS = 2
