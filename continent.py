from enum import Enum

from node import Node, find_node
from color import Color


class Continent():

    def __init__(self, name, nodes=[], single_owner=None):
        self.name = name
        self.nodes = nodes
        self.single_owner = single_owner

    def get_name(self):
        return self.name

    def get_nodes(self):
        return self.nodes

    def monopolize(self, owner):
        self.single_owner = owner

    def demonopolize(self):
        self.single_owner = None

    def find(self, nodeid):
        return find_node(nodeid, self.nodes)

    def change_owner(self, nodeid, new_owner):
        node = self.find(nodeid)
        node.set_owner(new_owner)


E1 = Node(21, "Iceland", Color.RED)
E2 = Node(22, "Great Britain", Color.GREEN)
E3 = Node(23, "Scandinavia", Color.YELLOW)
E4 = Node(24, "Western Europe", Color.GREEN)
E5 = Node(25, "Northern Europe", Color.YELLOW)
E6 = Node(26, "Ukraine")
E7 = Node(27, "Southern Europe", Color.BLUE)

E1.add_edge(E2)
E1.add_edge(E3)
E2.add_edge(E3)
E2.add_edge(E4)
E2.add_edge(E5)
E3.add_edge(E5)
E3.add_edge(E6)
E4.add_edge(E5)
E4.add_edge(E7)
E5.add_edge(E6)
E5.add_edge(E7)
E6.add_edge(E7)


Europe = Continent("Europe", [E1, E2, E3, E4, E5, E6, E7], None)
