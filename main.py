import random
import time

from continent import *
from roll import blitz

order = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]


def territories(player, continents):
    res = []
    for continent in continents:
        for node in continent.get_nodes():
            if node.get_owner() == player:
                res.append(node)
    return res


def blitz_attack(from_node, to_node):
    '''Conducts blitz attack between the two nodes and changes the results.
    Preconditions: from_node.get_troops() > 1 and to_node.get_troops() > 0;
    the nodes have two different owners.'''
    blitz_res = blitz(from_node.get_troops(), to_node.get_troops())

    if blitz_res[0] == 1:
        print("Attack unsuccessful! You now have 1 troop in " + from_node.get_name() + ". The " + to_node.get_owner().name +
              " player has " + str(blitz_res[1]) + " troops in " + to_node.get_name())
        from_node.set_troops(1)
        to_node.set_troops(blitz_res[1])
    elif blitz_res[1] == 0:
        print("Attack successful! You now have 1 troop in " + from_node.get_name() + " and " + str(blitz_res[0]-1) +
              " troops in " + to_node.get_name())
        print("You get a card!")
        from_node.set_troops(1)
        to_node.set_owner(curr_player)
        to_node.set_troops(blitz_res[0]-1)
    else:
        raise ValueError("Wrong results for blitz: (%i, %i)" % blitz_res)


def turn(curr_player):
    print("Current player: " + curr_player.name)
    print("Your currently owned territories: ")
    print(territories(curr_player, [Europe]))

    from_id = int(input("Enter the id of a node from which to attack: "))
    from_node = find_node(from_id, territories(curr_player, [Europe]))
    if from_node == None:
        print("You don't own a territory with such id! Please enter id of a territory you own!")
        turn(curr_player)
    elif from_node.get_troops() < 2:
        print("You need to have at least 2 troops in a territory to be able to attack!")
        turn(curr_player)
    else:
        options = from_node.attack_options()
        if len(options) == 0:
            print("You can't attack any nodes from the given node!")
            turn(curr_player)
        else:
            print("Possible nodes to attack: ", options)
            done = False
            while not done:
                to_id = int(input("Enter the id of a node which to attack: "))
                to_node = find_node(to_id, from_node.attack_options())
                if to_node == None:
                    print(
                        "Invalid node id! Node should be adjacent to the current node!")
                elif to_node.get_owner() == curr_player:
                    print("Territory already owned by you! Pick another territory.")
                else:
                    blitz_attack(from_node, to_node)
                    done = True


for node in Europe.nodes:
    node.set_troops(random.randint(1, 7))

print(Europe.nodes)

for i in range(4):
    curr_player = order.pop(0)
    order.append(curr_player)
    turn(curr_player)
