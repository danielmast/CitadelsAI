from enum import Enum


class Action(Enum):
    # Phase: CHOOSE_CHARACTERS
    CHOOSE_ASSASSIN = 0
    CHOOSE_THIEF = 1
    CHOOSE_MAGICIAN = 2
    CHOOSE_KING = 3
    CHOOSE_BISHOP = 4
    CHOOSE_MERCHANT = 5
    CHOOSE_ARCHITECT = 6
    CHOOSE_WARLORD = 7

    # Phase: PLAY_TURN
    DO_NOTHING = 8
    TAKE_TWO_GOLD = 9


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

    # Other actions
    TAKE_TWO_GOLD = 7
    DRAW_DISTRICTS = 8
    RECEIVE_CITY_GOLD = 9
    DISCARD_AND_DRAW = 10  # Magician only
    RECEIVE_EXTRA_GOLD = 11  # Merchant only
    DRAW_EXTRA_DISTRICTS = 12  # Architect only
    END_TURN = 13


class ActionObject(Enum):
    # Characters
    ASSASSIN = 0
    THIEF = 1
    MAGICIAN = 2
    KING = 3
    BISHOP = 4
    MERCHANT = 5
    ARCHITECT = 6
    WARLORD = 7
    
    # Players
    PLAYER_2 = 8
    PLAYER_3 = 9
    PLAYER_4 = 10
    
    # Districts
    TAVERN_1 = 11
    TAVERN_2 = 12
    TAVERN_3 = 13
    TAVERN_4 = 14
    TAVERN_5 = 15
    MARKET_1 = 16
    MARKET_2 = 17
    MARKET_3 = 18
    MARKET_4 = 19
    TRADING_POST_1 = 20
    TRADING_POST_2 = 21
    TRADING_POST_3 = 22
    DOCKS_1 = 23
    DOCKS_2 = 24
    DOCKS_3 = 25
    HARBOR_1 = 26
    HARBOR_2 = 27
    HARBOR_3 = 28
    TOWN_HALL_1 = 29
    TOWN_HALL_2 = 30

    TEMPLE_1 = 31
    TEMPLE_2 = 32
    TEMPLE_3 = 33
    CHURCH_1 = 34
    CHURCH_2 = 35
    CHURCH_3 = 36
    MONASTERY_1 = 37
    MONASTERY_2 = 38
    MONASTERY_3 = 39
    CATHEDRAL_1 = 40
    CATHEDRAL_2 = 41

    WATCH_TOWER_1 = 42
    WATCH_TOWER_2 = 43
    WATCH_TOWER_3 = 44
    PRISON_1 = 45
    PRISON_2 = 46
    PRISON_3 = 47
    BATTLEFIELD_1 = 48
    BATTLEFIELD_2 = 49
    BATTLEFIELD_3 = 50
    FORTRESS_1 = 51
    FORTRESS_2 = 52

    MANOR_1 = 53
    MANOR_2 = 54
    MANOR_3 = 55
    MANOR_4 = 56
    MANOR_5 = 57
    CASTLE_1 = 58
    CASTLE_2 = 59
    CASTLE_3 = 60
    CASTLE_4 = 61
    PALACE_1 = 62
    PALACE_2 = 63
    PALACE_3 = 64

    HAUNTED_CITY = 65
    KEEP_1 = 66
    KEEP_2 = 67
    LABORATORY = 68
    SMITHY = 69
    GRAVEYARD = 70
    OBSERVATORY = 71
    SCHOOL_OF_MAGIC = 72
    LIBRARY = 73
    GREAT_WALL = 74
    UNIVERSITY = 75
    DRAGON_GATE = 76
