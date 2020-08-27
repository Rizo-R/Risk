from troop import Troop


class Card:
    # Uniqueness of a card is defined by the territory it represents.
    def __init__(self, troop_type, territory):
        self.troop_type = troop_type
        self.territory = territory

    def get_info(self):
        return self.troop_type, self.territory


def add_card(card, card_lst):
    '''
    Uses binary search to add the given Card object to the given Card list.
    If [card] is already in [card_lst], raises ValueError.
    Returns a new list of Card objects.
    Preconditions: [card] is a Card object; [card_lst] is a list of Card objects
        that are sorted by territory name in an increasing order with no 
        duplicates. [card_lst] can be empty.
    '''
    if len(card_lst) == 0:
        return [card]

    i = len(card_lst) // 2
    curr_terr = card_lst[i].get_info[1]
    given_terr = card.get_info[1]

    if curr_terr < given_terr:
        return card_lst[:i+1] + add_card(card, card_lst[i+1:])
    elif curr_terr > given_terr:
        return add_card(card, card_lst[:i]) + card_lst[i:]
    raise ValueError("Card already in the card list!")


def remove_card(card_name, card_lst):
    '''
    Uses binary search to remove the card with given territory from 
        the given Card list.
    Returns a new list of Card objects. If the card is not found, raises 
        ValueError.
    Preconditions: [card_name] is a string; [card_lst] is a list of Card objects
        that are sorted by territory name in an increasing order with no 
        duplicates. [card_lst] can be empty.
    '''
    if len(card_lst) == 0:
        raise ValueError("Card not found in the card list!")

    i = len(card_lst) // 2
    curr_terr = card_lst[i].get_info[1]

    if curr_terr < card_name:
        return card_lst[:i+1] + remove_card(card_name, card_lst[i+1:])
    elif curr_terr > card_name:
        return remove_card(card_name, card_lst[:i]) + card_lst[i:]
    return card_lst[:i] + card_lst[i+1:]


def find_card(card_name, card_lst):
    '''
    Uses binary search to find the card with given territory in the given 
        Card list.
    Returns a Card object. If the card is not in [card_lst], returns None.
    Preconditions: [card] is a string; [card_lst] is a list of Card objects
        that are sorted by territory name in an increasing order with no 
        duplicates. [card_lst] can be empty.
    '''
    if len(card_lst) == 0:
        return None

    i = len(card_lst) // 2
    curr_terr = card_lst[i].get_info[1]

    if curr_terr < card_name:
        return find_card(card_name, card_lst[i+1:])
    elif curr_terr > card_name:
        return find_card(card_name, card_lst[:i])
    return card_lst[i]
