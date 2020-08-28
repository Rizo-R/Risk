from color import Color
from card import Card, add_card, find_card, remove_card


class Player():
    def __init__(self, color, troops, cards=[]):
        ''' [color] is a Color object. [troops] is int. [cards] is a list of
        Card objects. No duplicates, i.e. each player has their own unique 
        color.
        Note: [troops] refers to new troops that the player gets in the 
            beginning of each turn, as well as the initial troops they have 
            during territory claim in the very beginning of the game.'''
        self.color = color
        self.troops = troops
        self.cards = cards

    def get_color(self):
        return self.color

    def get_troops(self):
        return self.troops

    def set_troops(self, troops):
        self.troops = troops

    def add_troops(self, troops):
        self.troops += troops

    def subtract_troops(self, troops):
        self.troops -= troops

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
