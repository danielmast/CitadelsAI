import random
from abc import ABC, abstractmethod

from character import CharacterState


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.gold = 0
        self.hand = []
        self.city = []

    @abstractmethod
    def choose_character(self, game, round):
        raise Exception('Should be implemented by sub class')

    def play_turn(self, game, round):
        raise Exception('Should be implemented by sub class')


class RandomPlayer(Player):
    def choose_character(self, game, round):
        return random.choice(round.get_deck_characters())

    def play_turn(self, game, round, character):
        if character.name() == 'Assassin':
            self.murder(round)
        elif character.name() == 'Thief':
            self.rob(round)
        else:
            print(self.name, 'does nothing')

    def murder(self, round):
        victim = None
        while victim is None or victim.name() == 'Assassin' or round.character_state[victim] == CharacterState.FACE_UP:
            victim = random.choice(list(round.character_state.keys()))
        print(self.name, 'murders the', victim.name())
        round.murdered_character = victim

    def rob(self, round):
        victim = None
        while victim is None or victim.name() == 'Assassin' or victim.name() == 'Thief' \
                or round.character_state[victim] == CharacterState.FACE_UP\
                or victim == round.murdered_character:
            victim = random.choice(list(round.character_state.keys()))
        print(self.name, 'robs the', victim.name())
        round.robbed_character = victim


def create_players(game, player_count):
    players = []
    for p in range(1, player_count + 1):
        players.append(RandomPlayer('Player {}'.format(p)))
    return players


def face_up_count(player_count):
    if player_count == 4:
        return 2
    elif player_count == 5:
        return 1
    elif player_count == 6 or player_count == 7:
        return 0
    else:
        raise ValueError('Invalid player count: {}'.format(player_count))
