from enum import Enum

from game.character import CharacterState
from phase import Phase


class Action:
    def __init__(self, a):
        self.object = ActionObject.NONE

        if a < 8:
            self.verb = ActionVerb.CHOOSE
            self.object = ActionObject(a + 1)
        elif a < 16:  # 8 <= a <= 15
            self.verb = ActionVerb.MURDER
            self.object = ActionObject(a - 7)
        elif a < 24:  # 16 <= a <= 23
            self.verb = ActionVerb.ROB
            self.object = ActionObject(a - 15)
        elif a < 27:
            self.verb = ActionVerb.EXCHANGE_HANDS
            self.object = ActionObject(a - 15)
        elif a < 93:
            self.verb = ActionVerb.BUILD
            self.object = ActionObject(a - 15)
        elif a < 159:
            self.verb = ActionVerb.DISCARD
            self.object = ActionObject(a - 81)
        elif a < 225:
            self.verb = ActionVerb.DESTROY
            self.object = ActionObject(a - 147)
        elif a == 225:
            self.verb = ActionVerb.TAKE_TWO_GOLD
        elif a == 226:
            self.verb = ActionVerb.DRAW_TWO_DISTRICTS
        elif a == 227:
            self.verb = ActionVerb.RECEIVE_CITY_GOLD
        elif a == 228:
            self.verb = ActionVerb.DISCARD_AND_DRAW
        elif a == 229:
            self.verb = ActionVerb.RECEIVE_EXTRA_GOLD
        elif a == 230:
            self.verb = ActionVerb.DRAW_EXTRA_DISTRICTS
        elif a == 231:
            self.verb = ActionVerb.END_TURN

    def is_valid(self, env):
        if env.game.round.phase == Phase.CHOOSE_CHARACTERS:
            return self.is_valid_choose_characters(env)
        else:
            return self.is_valid_player_turns(env)

    def is_valid_choose_characters(self, env):
        if self.verb == ActionVerb.CHOOSE:
            if self.object.is_character():
                if self.object.to_character(env.game).state == CharacterState.DECK:
                    return True, ''
                else:
                    return False, 'Chosen character is not in deck'
            else:
                return False, 'Object must be a character in Phase.CHOOSE_CHARACTERS'
        else:
            return False, 'Verb must be CHOOSE in Phase.CHOOSE_CHARACTERS'

    def is_valid_player_turns(self, env):
        if env.must_discard_district and self.verb != ActionVerb.DISCARD:
            return False, 'Must discard district'

        if self.verb == ActionVerb.END_TURN:
            if self.object == ActionObject.NONE:
                return True, ''
            else:
                return False, 'Object must be NONE when ending turn'
        elif self.verb == ActionVerb.TAKE_TWO_GOLD:
            if self.object == ActionObject.NONE:
                if env.can_take_two_gold:
                    return True, ''
                else:
                    return False, 'Cannot take 2 gold'
            else:
                return False, 'Object must be NONE when taking 2 gold'
        elif self.verb == ActionVerb.DRAW_TWO_DISTRICTS:
            if self.object == ActionObject.NONE:
                if env.can_draw_two_districts:
                    if len(env.game.district_deck) >= 2:
                        return True, ''
                    else:
                        return False, 'Cannot take two districts (deck has less than two cards)'
                else:
                    return False, 'Cannot take two districts'
            else:
                return False, 'Object must be NONE when drawing 2 districts'
        elif self.verb == ActionVerb.DISCARD:
            if env.must_discard_district:
                if self.object.is_district():
                    if env.game.round.current_player.has_drawn(self.object.to_district(env.game)):
                        return True, ''
                    else:
                        return False, 'Must discard just drawn district'
                else:
                    return False, 'Object must be a district'
            else:
                return False, 'Cannot discard district'
        elif self.verb == ActionVerb.BUILD:
            if env.can_build:
                if self.object.is_district():
                    district = self.object.to_district(env.game)
                    if env.game.round.current_player.has_in_hand(district):
                        if env.game.round.current_player.can_build(district):
                            return True, ''
                        else:
                            return False, 'Not enough gold to build district'
                    else:
                        return False, 'District must be in hand'
                else:
                    return False, 'Object must be a district'
            else:
                return False, 'Cannot build district'
        else:
            return False, 'Unsupported verb in Phase.PLAYER_TURNS'


class ActionVerb(Enum):
    # Character actions
    CHOOSE = 0
    MURDER = 1  # Assassin only
    ROB = 2  # Thief only

    # Player actions
    EXCHANGE_HANDS = 3  # Magician only

    # District actions
    BUILD = 4
    DISCARD = 5
    DESTROY = 6  # Warlord only

    # Other actions (without object)
    TAKE_TWO_GOLD = 7
    DRAW_TWO_DISTRICTS = 8
    RECEIVE_CITY_GOLD = 9
    DISCARD_AND_DRAW = 10  # Magician only
    RECEIVE_EXTRA_GOLD = 11  # Merchant only
    DRAW_EXTRA_DISTRICTS = 12  # Architect only
    END_TURN = 13


class ActionObject(Enum):
    NONE = 0

    # Characters
    ASSASSIN = 1
    THIEF = 2
    MAGICIAN = 3
    KING = 4
    BISHOP = 5
    MERCHANT = 6
    ARCHITECT = 7
    WARLORD = 8

    # Players
    PLAYER_2 = 9
    PLAYER_3 = 10
    PLAYER_4 = 11

    # Districts
    TAVERN_1 = 12
    TAVERN_2 = 13
    TAVERN_3 = 14
    TAVERN_4 = 15
    TAVERN_5 = 16
    MARKET_1 = 17
    MARKET_2 = 18
    MARKET_3 = 19
    MARKET_4 = 20
    TRADING_POST_1 = 21
    TRADING_POST_2 = 22
    TRADING_POST_3 = 23
    DOCKS_1 = 24
    DOCKS_2 = 25
    DOCKS_3 = 26
    HARBOR_1 = 27
    HARBOR_2 = 28
    HARBOR_3 = 29
    TOWN_HALL_1 = 30
    TOWN_HALL_2 = 31

    TEMPLE_1 = 32
    TEMPLE_2 = 33
    TEMPLE_3 = 34
    CHURCH_1 = 35
    CHURCH_2 = 36
    CHURCH_3 = 37
    MONASTERY_1 = 38
    MONASTERY_2 = 39
    MONASTERY_3 = 40
    CATHEDRAL_1 = 41
    CATHEDRAL_2 = 42

    WATCH_TOWER_1 = 43
    WATCH_TOWER_2 = 44
    WATCH_TOWER_3 = 45
    PRISON_1 = 46
    PRISON_2 = 47
    PRISON_3 = 48
    BATTLEFIELD_1 = 49
    BATTLEFIELD_2 = 50
    BATTLEFIELD_3 = 51
    FORTRESS_1 = 52
    FORTRESS_2 = 53

    MANOR_1 = 54
    MANOR_2 = 55
    MANOR_3 = 56
    MANOR_4 = 57
    MANOR_5 = 58
    CASTLE_1 = 59
    CASTLE_2 = 60
    CASTLE_3 = 61
    CASTLE_4 = 62
    PALACE_1 = 63
    PALACE_2 = 64
    PALACE_3 = 65

    HAUNTED_CITY = 66
    KEEP_1 = 67
    KEEP_2 = 68
    LABORATORY = 69
    SMITHY = 70
    GRAVEYARD = 71
    OBSERVATORY = 72
    SCHOOL_OF_MAGIC = 73
    LIBRARY = 74
    GREAT_WALL = 75
    UNIVERSITY = 76
    DRAGON_GATE = 77

    def is_character(self):
        return 1 <= self.value <= 8

    def is_player(self):
        return 9 <= self.value <= 11

    def is_district(self):
        return 12 <= self.value <= 77

    def to_character(self, game):
        if self == ActionObject.ASSASSIN:
            return game.get_character('Assassin')
        elif self == ActionObject.THIEF:
            return game.get_character('Thief')
        elif self == ActionObject.MAGICIAN:
            return game.get_character('Magician')
        elif self == ActionObject.KING:
            return game.get_character('King')
        elif self == ActionObject.BISHOP:
            return game.get_character('Bishop')
        elif self == ActionObject.MERCHANT:
            return game.get_character('Merchant')
        elif self == ActionObject.ARCHITECT:
            return game.get_character('Architect')
        elif self == ActionObject.WARLORD:
            return game.get_character('Warlord')

    def to_district(self, game):
        return game.districts[self.value - 12]
