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
    deck = [District('Tavern', 1, Color.GREEN),
            District('Tavern', 1, Color.GREEN),
            District('Tavern', 1, Color.GREEN),
            District('Tavern', 1, Color.GREEN),
            District('Tavern', 1, Color.GREEN),
            District('Market', 2, Color.GREEN),
            District('Market', 2, Color.GREEN),
            District('Market', 2, Color.GREEN),
            District('Market', 2, Color.GREEN),
            District('Temple', 1, Color.BLUE),
            District('Temple', 1, Color.BLUE),
            District('Temple', 1, Color.BLUE),
            District('Watch tower', 1, Color.RED),
            District('Watch tower', 1, Color.RED),
            District('Watch tower', 1, Color.RED),
            District('Manor', 3, Color.YELLOW),
            District('Manor', 3, Color.YELLOW),
            District('Manor', 3, Color.YELLOW),
            District('Manor', 3, Color.YELLOW),
            District('Manor', 3, Color.YELLOW)]

    random.shuffle(deck)
    return deck
