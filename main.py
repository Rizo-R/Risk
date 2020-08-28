import random
import time

from color import Color
from continent import *
from roll import blitz
from player import Player


# Initialize players.
initial_troops = 30
red = Player(Color.RED, initial_troops, [])
blue = Player(Color.BLUE, initial_troops, [])
green = Player(Color.GREEN, initial_troops, [])
yellow = Player(Color.YELLOW, initial_troops, [])

# Randomize order.
order = [red, green]
random.shuffle(order)


def territories(color, continents):
    '''Returns a list of territories (Node list) owned by a player with a 
    given color in the given continent list (can be empty).'''
    res = []
    for continent in continents:
        for node in continent.get_nodes():
            if node.get_owner() == color:
                res.append(node)
    return res


def find_player(color, player_lst):
    '''Returns the player from [player_lst] with a given color. Raises
    ValueError if not found.'''
    for player in player_lst:
        if player.get_color() == color:
            return player
    raise ValueError('Player with color %s not found!' % str(color))


# WARNING: this function changes both [order] and [nodes].
def claim_territories(order, nodes):
    '''Gives territories for a given [order] in a given territories.'''
    while len(nodes) > 0:
        # Select the next player in the queue.
        curr_player = order.pop(0)
        order.append(curr_player)
        if curr_player.get_troops() == 0:
            continue
        # Get necessary information and pop the first node from [nodes].
        curr_color = curr_player.get_color()
        curr_node = nodes.pop(0)
        assert curr_node.get_troops() == -1, "Non-empty territory during claim!"
        # Set ownership and subtract troops.
        curr_node.set_owner(curr_color)
        curr_node.set_troops(1)
        curr_player.subtract_troops(1)
    return


def initialize_troops(order, nodes):
    # WARNING: this function changes both [order] and [nodes].
    '''Initializes troops using a given order in given node list.'''
    total_remaining_troops = 0
    for player in order:
        total_remaining_troops += player.get_troops()
    while total_remaining_troops > 0:
        # Pop the first node from the queue and put it at the end.
        curr_node = nodes.pop(0)
        nodes.append(curr_node)
        curr_color = curr_node.get_owner()
        # Find player with a given color.
        curr_player = find_player(curr_color, order)
        # Add a random number or, if the player doesn't have enough troops,
        # the remaining troops to the territory
        assigned_troops = min(random.randint(0, 5), curr_player.get_troops())
        curr_node.add_troops(assigned_troops)
        curr_player.subtract_troops(assigned_troops)
        total_remaining_troops -= assigned_troops


def remove_defeated(player_lst):
    '''Removes players with no territories from the given player list.
    Returns a new player list without the defeated players.
    Preconditions: no duplicates in [player_lst].'''
    res = []
    for i in range(len(player_lst)):
        player = player_lst[i]
        if len(territories(player.get_color(), continents)) > 0:
            res.append(player)
        else:
            print("\nThe %s Player has been defeated!\n" %
                  str(player.get_color()))
    return res


def check_attack(color, continents):
    '''Checks if the player with a given color can perform an attack.
    Returns a boolean.'''
    # First, check if there is at least one node where the player has more
    # than one unit. Next, for each node with more than 1 troop, check if there
    # are any adjacent enemy territories that could be attacked.
    for node in territories(color, continents):
        if node.get_troops() > 1 and len(node.attack_options()) > 0:
            return True
    return False


def check_attack_everyone(order, continents):
    '''Runs check_attack() on every remaining player to make sure at least 
    one player can attack.'''
    for player in order:
        if check_attack(player.get_color(), continents):
            return True
    return False


def blitz_attack(from_node, to_node):
    '''Conducts blitz attack between the two nodes and changes the results.
    Preconditions: from_node.get_troops() > 1 and to_node.get_troops() > 0;
    the nodes have two different owners.'''
    blitz_res = blitz(from_node.get_troops(), to_node.get_troops())

    if blitz_res[0] == 1:
        print("Attack unsuccessful! You now have 1 troop in " + from_node.get_name() + ". The " + str(to_node.get_owner()) +
              " player has " + str(blitz_res[1]) + " troops in " + to_node.get_name())
        from_node.set_troops(1)
        to_node.set_troops(blitz_res[1])
    elif blitz_res[1] == 0:
        print("Attack successful! You now have 1 troop in " + from_node.get_name() + " and " + str(blitz_res[0]-1) +
              " troops in " + to_node.get_name())
        print("You get a card!")
        from_node.set_troops(1)
        curr_color = from_node.get_owner()
        to_node.set_owner(curr_color)
        to_node.set_troops(blitz_res[0]-1)
    else:
        raise ValueError("Wrong results for blitz: (%i, %i)" % blitz_res)


def turn(curr_color):
    print("\nCurrent player: %s.\n" % str(curr_color))
    print("Your currently owned territories: ")
    print(territories(curr_color, continents))

    # Check if current player can attack.
    if not check_attack(curr_color, continents):
        print("Sorry, but you currently don't have any opportunities to attack!")
        return

    try:
        from_id = int(input("Enter the id of a node from which to attack: "))
    except ValueError:
        print("Invalid input!")
        turn(curr_color)
        return

    from_node = find_node(from_id, territories(curr_color, continents))
    if from_node == None:
        print("You don't own a territory with such id! Please enter id of a territory you own!")
        turn(curr_color)
    elif from_node.get_troops() < 2:
        print("You need to have at least 2 troops in a territory to be able to attack!")
        turn(curr_color)
    else:
        options = from_node.attack_options()
        if len(options) == 0:
            print("You can't attack any nodes from the given node!")
            turn(curr_color)
        else:
            print("You have %i troops in %s." %
                  (from_node.get_troops(), from_node.get_name()))
            print("Possible nodes to attack: ", options)
            done = False
            while not done:
                to_id = int(input("Enter the id of a node which to attack: "))
                to_node = find_node(to_id, from_node.get_neighbors())
                if to_node == None:
                    print(
                        "Invalid node id! Node should be adjacent to the current node!")
                elif to_node.get_owner() == curr_color:
                    print("Territory already owned by you! Pick another territory.")
                else:
                    blitz_attack(from_node, to_node)
                    done = True


# Because of colored printing, printing nodes owned by Color.NONE will result
# in TypeError (since Color.None.Value is int).
# print(Europe.nodes)


claim_territories(order, all_nodes.copy())
initialize_troops(order, all_nodes.copy())
# Ensure there are no unowned nodes.
for continent in continents:
    for node in continent.get_nodes():
        if node.get_owner() == Color.NONE:
            raise ValueError('Unowned node!' + str(node))


game_over = False
while not game_over:
    order = remove_defeated(order)
    # Check if there's a victor.
    if len(order) == 1:
        print("\n\nThe %s Player won! Congratulations!\n\n" %
              str(order[0].get_color()))
        game_over = True
    # Check if at least one player can attack.
    elif not check_attack_everyone(order, continents):
        print("\n\nNo one else can attack anymore! End of the game!\n\n")
        game_over = True
    else:
        curr_player = order.pop(0)
        order.append(curr_player)
        turn(curr_player.get_color())
