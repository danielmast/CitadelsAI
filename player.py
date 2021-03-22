import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name):
        self.name = name
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

    def play_turn(self, game, round):
        print('Do nothing')


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
