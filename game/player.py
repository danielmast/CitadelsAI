import random
from abc import ABC, abstractmethod

from stable_baselines3 import A2C

from game.character import CharacterState, Assassin, Thief, Magician, ColorCharacter, Merchant, Architect, Warlord
from game.color import Color


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.gold = 0
        self.hand = []
        self.city = []

    @abstractmethod
    def choose_character(self, game, round):
        raise Exception('Should be implemented by sub class')

    @abstractmethod
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

        if len(colors) == 4 and self.number_of_districts_of_color(Color.PURPLE) >= 2 \
                and self.has_built('Haunted City'):
            return True

        return False

    def number_of_districts_of_color(self, color):
        number = 0
        for district in self.city:
            if district.color == color:
                number += 1
        return number

    def has_built(self, district_name):
        for district in self.city:
            if district.name == district_name:
                return True
        return False

    def draw_district(self, game):
        print(self.name, 'grabs a district')
        district = game.district_deck.pop()
        self.hand.append(district)
        return district

    def allowed_to_draw_number(self):
        if self.has_built('Observatory'):
            return 3
        return 2

    def allowed_to_keep_number(self):
        if self.has_built('Library'):
            return 2
        return 1

    def discard_district(self, game, district):
        print(self.name, 'discards a district')
        self.hand.remove(district)
        game.district_deck.insert(0, district)

    def take_2_gold(self):
        print(self.name, 'takes 2 gold')
        self.gold += 2

    def build_district(self, district):
        self.hand.remove(district)
        print(self.name, 'builds a', district.name)
        self.city.append(district)
        self.gold -= district.cost


class AgentPlayer(Player):
    def __init__(self, name, model):
        super(AgentPlayer, self).__init__(name)
        self.model = model

    def choose_character(self, game, round):
        return random.choice(round.get_deck_characters())

    def play_turn(self, game, round, character):
        print('I\'m a lazy agent doing nothing yet')
        pass


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
            self.take_2_gold()
        else:
            self.draw_districts(game)

        if isinstance(character, Merchant):
            Merchant.receive_extra_gold(self)
        elif isinstance(character, Architect):
            Architect.draw_extra_districts(self, game)

        if random_boolean() and self.buildable_districts():
            district = random.choice(self.buildable_districts())
            self.build_district(district)

        if isinstance(character, Architect):
            for i in range(0, random.randint(0, 2)):
                if self.buildable_districts():
                    district = random.choice(self.buildable_districts())
                    self.build_district(district)

        if isinstance(character, ColorCharacter):
            if not has_received_city_gold:
                character.receive_city_gold(self)

        if isinstance(character, Warlord) and random_boolean():
            victim_player = None
            while victim_player is None or victim_player == round.get_player_by_character(game.get_character('Bishop')):
                victim_player = self.random_other_player(game)

            victim_city = victim_player.city.copy()
            random.shuffle(victim_city)

            has_destroyed_district = False
            for district in victim_city:
                if not has_destroyed_district and Warlord.can_destroy_district(self, victim_player, district, round):
                    Warlord.destroy_district(self, victim_player, district)
                    has_destroyed_district = True


    @staticmethod
    def murder(round):
        victim = None
        while victim is None or isinstance(victim, Assassin) or round.game.character_state[victim].state == CharacterState.FACE_UP:
            victim = random.choice(list(round.game.character_state.keys()))
        Assassin.murder(victim, round)

    @staticmethod
    def rob(round):
        victim = None
        while victim is None or isinstance(victim, Assassin) or isinstance(victim, Thief) \
                or round.game.character_state[victim].state == CharacterState.FACE_UP\
                or victim == round.murdered_character:
            victim = random.choice(list(round.game.character_state.keys()))
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
        drawn = []
        for i in range(0, min(len(game.district_deck), self.allowed_to_draw_number())):
            drawn.append(self.draw_district(game))

        for i in range(0, min(len(drawn), self.allowed_to_draw_number() - self.allowed_to_keep_number())):
            d = random.choice(drawn)
            drawn.remove(d)
            self.discard_district(game, d)

    def buildable_districts(self):
        affordable = []
        for district in self.hand:
            if district.cost <= self.gold and not self.has_built(district.name):
                affordable.append(district)
        return affordable


def random_boolean():
    return random.randint(0, 1) == 0


def create_players(game, player_count):
    players = []
    players.append(create_agent_player())
    for p in range(2, player_count + 1):
        players.append(RandomPlayer('Player {}'.format(p)))
    return players


def create_agent_player():
    model = None
    return AgentPlayer('Agent', model)


def face_up_count(player_count):
    if player_count == 4:
        return 2
    elif player_count == 5:
        return 1
    elif player_count == 6 or player_count == 7:
        return 0
    else:
        raise ValueError('Invalid player count: {}'.format(player_count))
