from color import Color
from card import Card, add_card, find_card, remove_card


class Player():
    def __init__(self, color, troops, cards=[]):
        ''' [color] is a Color object. [troops] is int. [cards] is a list of
        Card objects.'''
        self.color = color
        self.troops = troops
        self.cards = cards

    # Note: [card] must be a Card object.
    def give_card(self, card):
        self.cards = add_card(card, self.cards)

    # Note: [card_name] must be a name of a territory owned by player.
    def take_card(self, card_name):
        '''Returns the card with given [card_name] while removing it from 
        the player's hand.'''
        card = find_card(card_name, self.cards)
        self.cards = remove_card(card_name, self.cards)
        return card
