import random
from abc import ABC

from color import Color


class Character(ABC):
    def name(self):
        return type(self).__name__


class Assassin(Character):
    def __init__(self):
        self.color = Color.NONE

    @staticmethod
    def murder(character, round):
        round.murdered = character


class Thief(Character):
    def __init__(self):
        self.color = Color.NONE


class Magician(Character):
    def __init__(self):
        self.color = Color.NONE


class King(Character):
    def __init__(self):
        self.color = Color.YELLOW


class Bishop(Character):
    def __init__(self):
        self.color = Color.BLUE


class Merchant(Character):
    def __init__(self):
        self.color = Color.GREEN


class Architect(Character):
    def __init__(self):
        self.color = Color.NONE


class Warlord(Character):
    def __init__(self):
        self.color = Color.RED


def create_character_deck():
    deck = [Assassin(), Thief(), Magician(), King(), Bishop(), Merchant(), Architect(), Warlord()]
    random.shuffle(deck)
    return deck
