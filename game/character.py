from abc import ABC
from enum import Enum

from game.color import Color


class Character(ABC):
    def name(self):
        return type(self).__name__


class ColorCharacter(Character):
    def receive_city_gold(self, player):
        gold = 0
        for district in player.city:
            if district.color == self.color or district.name == 'School of Magic':
                gold += 1

        if gold > 0:
            print('The', self.name(), 'receives', gold, 'gold from the', self.color.name, 'districts in his city')
            player.gold += gold


class Assassin(Character):
    def __init__(self):
        self.color = Color.NONE

    @staticmethod
    def murder(character, round):
        print('The Assassin murders the', character.name())
        round.murdered_character = character


class Thief(Character):
    def __init__(self):
        self.color = Color.NONE

    @staticmethod
    def rob(character, round):
        print('The Thief robs the', character.name())
        round.robbed_character = character


class Magician(Character):
    def __init__(self):
        self.color = Color.NONE

    @staticmethod
    def exchange_hands(player, victim_player):
        print('The Magician exchanges hands with', victim_player.name)
        hand = player.hand.copy()
        player.hand = victim_player.hand
        victim_player.hand = hand

    @staticmethod
    def discard_and_draw(player, districts, game):
        print('The Magician discards', len(districts), 'districts and draws', len(districts), 'new districts')
        for district in districts:
            player.hand.remove(district)
            game.district_deck.insert(0, district)

        for i in range(0, len(districts)):
            player.hand.append(game.district_deck.pop())


class King(ColorCharacter):
    def __init__(self):
        self.color = Color.YELLOW


class Bishop(ColorCharacter):
    def __init__(self):
        self.color = Color.BLUE


class Merchant(ColorCharacter):
    def __init__(self):
        self.color = Color.GREEN

    @staticmethod
    def receive_extra_gold(player):
        print('The Merchant receives 1 extra gold')
        player.gold += 1


class Architect(Character):
    def __init__(self):
        self.color = Color.NONE

    @staticmethod
    def draw_extra_districts(player, game):
        drawn = 0
        for i in range(0, 2):
            if len(game.district_deck) > 0:
                player.hand.append(game.district_deck.pop())
                drawn += 1

        if drawn > 0:
            print('The Architect draws', drawn, 'extra districts')


class Warlord(ColorCharacter):
    def __init__(self):
        self.color = Color.RED

    @staticmethod
    def destroy_cost(victim_player, district):
        if victim_player.has_built('Great Wall') and district.name != 'Great Wall':
            return district.cost
        return district.cost - 1

    @staticmethod
    def can_destroy_district(player, victim_player, district, round):
        return round.get_player_by_character(round.game.get_character('Bishop')) != victim_player \
               and district.name != 'Keep' \
               and len(victim_player.city) < 8 \
               and player.gold >= Warlord.destroy_cost(victim_player, district)

    @staticmethod
    def destroy_district(player, victim_player, district):
        print('The Warlord destroys the', district.name, 'of', victim_player.name)
        player.gold -= Warlord.destroy_cost(victim_player, district)
        victim_player.city.remove(district)


class CharacterState:
    DECK = 1
    FACE_UP = 2
    FACE_DOWN = 3
    CHOSEN = 4

    def __init__(self):
        self.state = CharacterState.DECK
        self.player = None

    def reset(self):
        self.state = CharacterState.DECK
        self.player = None

    def set_player(self, player):
        self.state = CharacterState.CHOSEN
        self.player = player