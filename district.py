import random

from color import Color


class District:
    def __init__(self, name, cost, color, value=None):
        self.name = name
        self.cost = cost
        self.color = color

        if value is None:
            self.value = cost
        else:
            self.value = value


def create_deck():
    deck = [tavern(),
            tavern(),
            tavern(),
            tavern(),
            tavern(),
            market(),
            market(),
            market(),
            market(),
            trading_post(),
            trading_post(),
            trading_post(),
            docks(),
            docks(),
            docks(),
            harbor(),
            harbor(),
            harbor(),
            town_hall(),
            town_hall(),

            temple(),
            temple(),
            temple(),
            church(),
            church(),
            church(),
            monastery(),
            monastery(),
            monastery(),
            cathedral(),
            cathedral(),

            watch_tower(),
            watch_tower(),
            watch_tower(),
            prison(),
            prison(),
            prison(),
            battlefield(),
            battlefield(),
            battlefield(),
            fortress(),
            fortress(),

            manor(),
            manor(),
            manor(),
            manor(),
            manor(),
            castle(),
            castle(),
            castle(),
            castle(),
            palace(),
            palace(),
            palace(),

            haunted_city(),
            keep(),
            keep(),
            laboratory(),
            smithy(),
            graveyard(),
            observatory(),
            school_of_magic(),
            library(),
            # great_wall(),
            university(),
            dragon_gate()
    ]

    random.shuffle(deck)
    return deck


def tavern(): return District('Tavern', 1, Color.GREEN)
def market(): return District('Market', 2, Color.GREEN)
def trading_post(): return District('Trading Post', 2, Color.GREEN)
def docks(): return District('Docks', 3, Color.GREEN)
def harbor(): return District('Harbor', 4, Color.GREEN)
def town_hall(): return District('Town Hall', 5, Color.GREEN)


def temple(): return District('Temple', 1, Color.BLUE)
def church(): return District('Church', 2, Color.BLUE)
def monastery(): return District('Monastery', 3, Color.BLUE)
def cathedral(): return District('Cathedral', 5, Color.BLUE)


def watch_tower(): return District('Watch Tower', 1, Color.RED)
def prison(): return District('Prison', 2, Color.RED)
def battlefield(): return District('Battlefield', 3, Color.RED)
def fortress(): return District('Fortress', 5, Color.RED)


def manor(): return District('Manor', 3, Color.YELLOW)
def castle(): return District('Castle', 4, Color.YELLOW)
def palace(): return District('Palace', 5, Color.YELLOW)


def haunted_city(): return District('Haunted City', 2, Color.PURPLE)
def keep(): return District('Keep', 3, Color.PURPLE)
def laboratory(): return District('Laboratory', 5, Color.PURPLE)
def smithy(): return District('Smithy', 5, Color.PURPLE)
def graveyard(): return District('Graveyard', 5, Color.PURPLE)
def observatory(): return District('Observatory', 5, Color.PURPLE)
def school_of_magic(): return District('School of Magic', 6, Color.PURPLE)
def library(): return District('Library', 6, Color.PURPLE)
def great_wall(): return District('Great Wall', 6, Color.PURPLE)
def university(): return District('University', 6, Color.PURPLE, 8)
def dragon_gate(): return District('Dragon Gate', 6, Color.PURPLE, 8)
