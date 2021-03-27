import random

import district
from round import Round
import player


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = player.create_players(self, player_count)
        self.district_deck = district.create_deck()
        self.next_crown_player = random.choice(self.players)
        self.first_finished_player = None

    def start(self):
        print(self.player_count, 'players')
        for p in self.players:
            p.gold = 2
            for i in range(4):
                p.hand.append(self.district_deck.pop())

        print('Start game')
        round_number = 1
        while not self.end_of_game():
            r = Round(self, round_number, self.next_crown_player)
            r.start()
            round_number += 1
        print('End of game')

        print('Points:')
        for player in self.players:
            print(player.name, ':', player.points(self))

        winner = self.winner()
        if isinstance(winner, list):
            for w in winner:
                print('Winner:', w.name)
        else:
            print('Winner:', winner.name)

    def end_of_game(self):
        for player in self.players:
            if len(player.city) >= 8:
                return True
        return False

    def winner(self):
        max_points = -1
        max_city_value = -1
        max_gold = -1
        for player in self.players:
            if player.points(self) > max_points:
                max_points = player.points(self)
                if player.city_value() > max_city_value:
                    max_city_value = player.city_value()
                    if player.gold > max_gold:
                        max_gold = player.gold

        players_with_max_points = []
        players_with_max_city_value = []
        players_with_max_gold = []
        for player in self.players:
            if player.points(self) == max_points:
                players_with_max_points.append(player)
                if player.city_value() == max_city_value:
                    players_with_max_city_value.append(player)
                    if player.gold == max_gold:
                        players_with_max_gold.append(player)

        if len(players_with_max_points) > 1:
            if len(players_with_max_city_value) > 1:
                if len(players_with_max_gold) > 1:
                    return players_with_max_gold
                else:
                    return players_with_max_gold[0]
            else:
                return players_with_max_city_value[0]
        else:
            return players_with_max_points[0]
