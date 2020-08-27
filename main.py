from continent import *
import random
import time

order = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]


def territories(player, continents):
    res = []
    for continent in continents:
        for node in continent.get_nodes():
            if node.get_owner() == player:
                res.append(node)
    return res


def turn(curr_player):
    print("Current player: " + curr_player.name)
    print("Your currently owned territories: ")
    print(territories(curr_player, [Europe]))

    from_id = int(input("Enter the id of a node from which to attack: "))
    from_node = find_node(from_id, territories(curr_player, [Europe]))
    if from_node == None:
        print("You don't own a territory with such id! Please enter id of a territory you own!")
        turn(curr_player)
    else:
        done = False
        while not done:
            to_id = int(input("Enter the id of a node which to attack: "))
            # TODO: change to to_node.neighbors()
            to_node = find_node(to_id, Europe.get_nodes())
            if to_node == None:
                print("Invalid node id! Node should be adjacent to the current node!")
            elif to_node.get_owner() == curr_player:
                print("Territory already owned by you! Pick another territory.")
            else:
                attack = random.randint(1, 6)
                defend = random.randint(1, 6)

                if attack > defend:
                    to_node.set_owner(curr_player)
                    print("Attack successful!")
                    print("\nYou now own " + to_node.get_name() + ".")
                else:
                    print("Attack unsuccessful! NYEURRRRR")

                done = True


for node in Europe.nodes:
    node.set_troops(random.randint(1, 5))

print(Europe.nodes)

for i in range(4):
    curr_player = order.pop(0)
    order.append(curr_player)
    turn(curr_player)
