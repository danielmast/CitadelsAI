import random

# import district
from game import district, player
from game.round import Round


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = player.create_players(self, player_count)
        self.district_deck = district.create_deck()
        self.round = None
        self.next_crown_player = random.choice(self.players)
        self.first_finished_player = None

    def start_auto(self):
        print(self.player_count, 'players')
        for p in self.players:
            p.gold = 2
            for i in range(4):
                p.hand.append(self.district_deck.pop())

        print('Start game')
        round_number = 1
        while not self.end_of_game():
            r = Round(self, round_number, self.next_crown_player)
            r.start_auto()
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

    def start(self):
        print(self.player_count, 'players')
        for p in self.players:
            p.gold = 2
            for i in range(4):
                p.hand.append(self.district_deck.pop())

        print('Start game')
        self.set_next_round()

    def set_next_round(self):
        if self.round is None:
            round_number = 1
        else:
            round_number = self.round.number + 1
        self.round = Round(self, round_number, self.next_crown_player)

    def end(self):
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
        players_with_max_points = self.players_with_max_points()
        if len(self.players_with_max_points()) > 1:
            players_with_max_city_value = self.players_with_max_city_value(players_with_max_points)
            if len(players_with_max_city_value) > 1:
                players_with_max_gold = self.players_with_max_gold(players_with_max_city_value)
                if len(players_with_max_gold) > 1:
                    return players_with_max_gold
                else:
                    return players_with_max_gold[0]
            else:
                return players_with_max_city_value[0]
        else:
            return players_with_max_points[0]

    def players_with_max_points(self):
        players = self.players
        max_points = -1
        for player in players:
            if player.points(self) > max_points:
                max_points = player.points(self)

        players_with_max_points = []
        for player in players:
            if player.points(self) == max_points:
                players_with_max_points.append(player)

        return players_with_max_points

    def players_with_max_city_value(self, players):
        max_city_value = -1
        for player in players:
            if player.city_value() > max_city_value:
                max_city_value = player.city_value()

        players_with_max_city_value = []
        for player in players:
            if player.city_value() == max_city_value:
                players_with_max_city_value.append(player)

        return players_with_max_city_value

    def players_with_max_gold(self, players):
        max_gold = -1
        for player in players:
            if player.gold > max_gold:
                max_gold = player.gold

        players_with_max_gold = []
        for player in players:
            if player.gold == max_gold:
                players_with_max_gold.append(player)

        return players_with_max_gold
