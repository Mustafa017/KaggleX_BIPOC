# tutorial - https://realpython.com/python-data-classes/

from dataclasses import dataclass, field
from typing import List


@dataclass
class PlayingCard:
    rank: str
    suit: str


@dataclass
class Deck:
    cards: List[PlayingCard]


queen_of_hearts = PlayingCard('Q', 'Hearts')
ace_of_spades = PlayingCard('A', 'Spades')
two_cards = Deck([queen_of_hearts, ace_of_spades])
print(f'queen_of_hearts => {queen_of_hearts}')
print(f'ace_of_spades => {ace_of_spades}')
print(f'two_cards => {two_cards}')


# Advanced Default Values
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()


def make_french_deck():
    return [PlayingCard(r, s) for s in SUITS for r in RANKS]


# data classes use something called a default_factory to handle mutable default values. To use default_factory (and many other cool features of data classes), you need to use the field() specifier
@dataclass
class Deck2:
    cards: List[PlayingCard] = field(default_factory=make_french_deck)


print("\n\n")
print(Deck2())
