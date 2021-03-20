import random
from abc import ABC


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.city = []


class RandomPlayer(Player):
    def choose_character(self, game, round):
        c = round.character_deck.pop(random.randint(0, len(round.character_deck) - 1))
        print(self.name, 'chooses', c.name())
        return c


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
