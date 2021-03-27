import random
from abc import ABC, abstractmethod

from character import CharacterState, Assassin, Thief, Magician, ColorCharacter


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.gold = 0
        self.hand = []
        self.city = []

    @abstractmethod
    def choose_character(self, game, round):
        raise Exception('Should be implemented by sub class')

    def play_turn(self, game, round, character):
        raise Exception('Should be implemented by sub class')

    def points(self, game):
        points = self.city_value()
        if self.has_districts_of_each_color():
            points += 3
        if game.first_finished_player == self:
            points += 4
        elif len(self.city) == 8:
            points += 2
        return points

    def city_value(self):
        value = 0
        for district in self.city:
            value += district.value
        return value

    def has_districts_of_each_color(self):
        colors = []
        for district in self.city:
            if district.color not in colors and district.color is not None:
                colors.append(district.color)
        if len(colors) == 5:
            return True
        return False


class RandomPlayer(Player):
    def choose_character(self, game, round):
        return random.choice(round.get_deck_characters())

    def play_turn(self, game, round, character):
        has_received_city_gold = False

        if character.name() == 'Assassin':
            self.murder(round)
        elif character.name() == 'Thief':
            self.rob(round)
        elif character.name() == 'Magician':
            action = random.randint(0, 3)
            if action == 0:
                self.exchange_hands(game)
            elif action == 1 and len(self.hand) > 0:
                self.discard_and_draw(game)
        elif isinstance(character, ColorCharacter):
            if random_boolean():
                character.receive_city_gold(self)
                has_received_city_gold = True

        if random_boolean() or len(game.district_deck) < 2:
            print(self.name, 'takes 2 gold')
            self.gold += 2
        else:
            self.draw_districts(game)

        if random_boolean() and self.buildable_districts():
            self.build_district()

        if isinstance(character, ColorCharacter):
            if not has_received_city_gold:
                character.receive_city_gold(self)

    def murder(self, round):
        victim = None
        while victim is None or victim.name() == 'Assassin' or round.character_state[victim] == CharacterState.FACE_UP:
            victim = random.choice(list(round.character_state.keys()))
        Assassin.murder(victim, round)

    def rob(self, round):
        victim = None
        while victim is None or victim.name() == 'Assassin' or victim.name() == 'Thief' \
                or round.character_state[victim] == CharacterState.FACE_UP\
                or victim == round.murdered_character:
            victim = random.choice(list(round.character_state.keys()))
        Thief.rob(victim, round)

    def exchange_hands(self, game):
        victim_player = self.random_other_player(game)
        Magician.exchange_hands(self, victim_player)

    def discard_and_draw(self, game):
        districts = []

        if len(self.hand) == 1:
            districts.append(self.hand[0])
        else:
            shuffled_hand = self.hand.copy()
            random.shuffle(shuffled_hand)
            for i in range(0, random.randint(0, len(self.hand) - 1) + 1):
                districts.append(shuffled_hand[i])

        Magician.discard_and_draw(self, districts, game)

    def random_other_player(self, game):
        other_players = []
        for player in game.players:
            if player is not self:
                other_players.append(player)
        return random.choice(other_players)

    def take_gold(self):
        self.gold += 2

    def draw_districts(self, game):
        district1 = game.district_deck.pop()
        district2 = game.district_deck.pop()
        print(self.name, 'grabs 2 districts and keeps the', district1.name)
        self.hand.append(district1)
        game.district_deck.insert(0, district2)

    def buildable_districts(self):
        affordable = []
        for district in self.hand:
            if district.cost <= self.gold and not self.has_built(district.name):
                affordable.append(district)
        return affordable

    def has_built(self, district_name):
        for district in self.city:
            if district.name == district_name:
                return True
        return False

    def build_district(self):
        district = random.choice(self.buildable_districts())
        self.hand.remove(district)
        print(self.name, 'builds a', district.name)
        self.city.append(district)
        self.gold -= district.cost


def random_boolean():
    return random.randint(0, 1) == 0


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
