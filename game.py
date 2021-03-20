import random

import district
from round import Round
import player


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = player.create_players(self, player_count)
        self.districtDeck = district.create_deck()

    def start(self):
        print(self.player_count, 'players')
        for p in self.players:
            p.gold = 2
            for i in range(4):
                p.hand.append(self.districtDeck.pop())

        print('Start game')
        crown_player = random.choice(self.players)
        print(crown_player.name, 'receives the crown')
        r = Round(self, 1, crown_player)
        r.start()
