import random
import time

from color import Color
from continent import *
from roll import blitz
from player import Player


# Initialize players.
initial_troops = 7
red = Player(Color.RED, 80, [])
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


def calculate_troops_gained(curr_color, continents, print_details=False):
    '''Calculates the number of troops gained by the player with a given color
    in the beginning of their turn.
    Returns the number of gained troops (int), the number of territories owned
    by the player (int), and the list of continents owned by the player
    (Continent list).'''
    continents_owned = []
    territories_owned = len(territories(curr_color, continents))
    territory_bonus = max(territories_owned//3, 3)
    troops_gained = 0
    troops_gained += territory_bonus
    for continent in continents:
        if continent.get_owner() == curr_color:
            continents_owned.append(continent)
            bonus = continent.get_bonus()
            troops_gained += bonus
            if print_details:
                print("%i troops for %s," % (bonus, continent.get_name()))
    if print_details:
        print("%i troops for %i territories." %
              (territory_bonus, territories_owned))
    return troops_gained, territories_owned, continents_owned


def print_continent_list(continent_lst):
    '''Helper function for deploy_phase(). Returns a string.'''
    size = len(continent_lst)

    if size == 0:
        return ""
    elif size == 1:
        return continent_lst[0].get_name()
    elif size == 2:
        return "%s and %s" % (continent_lst[0].get_name(), continent_lst[1].get_name())
    return continent_lst[0].get_name() + ", " + print_continent_list(continent_lst[1:])


def request_input(input_type, msg):
    '''
    Helper function for deploy_phase(), attack_phase(), and fortify_phase().
    Requests input of a given [input_type] (either 'int', 'float', or 'str')
        with a given message (str) until user enters input of a type needed.
    Returns user's input.
    '''
    while True:
        try:
            res = input_type(input(msg))
            return res
        except ValueError:
            print("Invalid input!")


def set_continent_owners(continents):
    '''Checks if any of the continents is owned by a single color and
    sets owners if there are ones.'''
    for continent in continents:
        single_owner = True
        node_lst = continent.get_nodes()
        possible_owner = node_lst[0].get_owner()
        for node in node_lst[1:]:
            if node.get_owner() != possible_owner:
                single_owner = False
                continent.demonopolize()
                break
        if single_owner:
            continent.monopolize(possible_owner)


def deploy_phase(curr_player):
    print("\nDEPLOY.\n")
    curr_color = curr_player.get_color()
    assert curr_player.get_troops() == 0, "Undeployed troops for %s Player!" % curr_color
    troops_gained, _, _ = calculate_troops_gained(curr_color, continents, True)
    curr_player.set_troops(troops_gained)
    print("Total %i troops to deploy." % troops_gained)
    print("\nChoose where to put your troops.")

    msg_1 = "Your currently owned territories: \n" \
        + str(territories(curr_color, continents)) \
        + "\nEnter the id of a node where to put troops: "
    msg_2 = "Enter the number of troops to add: "

    # Keep placing troops until player has no more undeployed troops.
    while curr_player.get_troops() > 0:
        print("\nYou have %i more troops to deploy." %
              curr_player.get_troops())
        # Ask for a node id.
        nodeid = request_input(int, msg_1)
        node = find_node(nodeid, all_nodes_sorted)
        # Node not found.
        if node == None:
            print("\nNode with such id not found!")
            continue
        # Check ownership of the node.
        elif node.get_owner() != curr_color:
            print("\nYou don't own this territory!")
            continue
        # Ask for a number of troops to add.
        troops_added = request_input(int, msg_2)
        if troops_added < 0:
            print("\nNumber of deployed troops can't be negative!")
        elif troops_added > curr_player.get_troops():
            print("\nYou don't have that many troops to deploy!")
        else:
            node.add_troops(troops_added)
            curr_player.subtract_troops(troops_added)
            print("\nDone! You now have %i troops in %s." %
                  (node.get_troops(), node.get_name()))

    print("\nDone deploying troops.\n")


def attack_phase(curr_color):
    print("\nATTACK.\n")

    done_attacking = False
    while not done_attacking:
        # Check if current player can attack.
        if not check_attack(curr_color, continents):
            print("Sorry! You currently don't have any opportunities to attack!")
            return

        msg = "Your currently owned territories: \n" \
            + str(territories(curr_color, continents)) \
            + "\nEnter the id of a node from which to attack or -1 to finish ATTACK phase: "
        from_id = request_input(int, msg)

        # Check if done.
        if from_id == -1:
            done_attacking = True
            break

        from_node = find_node(from_id, territories(curr_color, continents))
        if from_node == None:
            print(
                "You don't own a territory with such id! Please enter id of a territory you own!")
            continue
        elif from_node.get_troops() < 2:
            print(
                "You need to have at least 2 troops in a territory to be able to attack!")
            continue
        else:
            options = from_node.attack_options()
            # Check if can attack from the node.
            if len(options) == 0:
                print("You can't attack any nodes from the given node!")
                continue
            else:
                print("You have %i troops in %s." %
                      (from_node.get_troops(), from_node.get_name()))
                print("Possible nodes to attack: ", options)
                to_id = request_input(
                    int, "Enter the id of a node to attack: ")
                to_node = find_node(to_id, from_node.get_neighbors())
                if to_node == None:
                    print(
                        "Invalid node id! Node should be adjacent to the current node!")
                elif to_node.get_owner() == curr_color:
                    print(
                        "Territory already owned by you! Pick another territory.")
                else:
                    blitz_attack(from_node, to_node)

                # done = False
                # while not done:
                #     to_id = int(
                #         input("Enter the id of a node which to attack: "))
                #     to_node = find_node(to_id, from_node.get_neighbors())
                #     if to_node == None:
                #         print(
                #             "Invalid node id! Node should be adjacent to the current node!")
                #     elif to_node.get_owner() == curr_color:
                #         print(
                #             "Territory already owned by you! Pick another territory.")
                #     else:
                #         blitz_attack(from_node, to_node)
                #         done = True


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
    # Remove defeated players.
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
    # Make a turn.
    else:
        curr_player = order.pop(0)
        order.append(curr_player)
        print("\nCurrent player: %s.\n" % str(curr_player.get_color()))
        set_continent_owners(continents)
        deploy_phase(curr_player)
        attack_phase(curr_player.get_color())
