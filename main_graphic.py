import math
import pygame
import random
import time

from main import *

pygame.init()

display_width = 1200
display_height = 900

black = (0, 0, 0)
grey = (50, 50, 50)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
brighter_red = (220, 0, 0)
brighter_green = (0, 220, 0)
brightest_red = (255, 0, 0)
brightest_green = (0, 255, 0)
blue = (0, 0, 255)

button_radius = 75

gameDisplay = pygame.display.set_mode(
    (display_width, display_height), pygame.RESIZABLE)
# gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("RISK")
clock = pygame.time.Clock()

bgImg_unscaled = pygame.image.load("map.png").convert()
bgImg = pygame.transform.scale(bgImg_unscaled, (display_width, display_height))

dim = 170
bright = 200
brightest = 255
colors = {
    "RED": [(dim, 0, 0), (bright, 0, 0), (brightest, 0, 0)],
    "YELLOW": [(dim, dim, 0), (bright, bright, 0), (brightest, brightest, 0)],
    "GREEN": [(0, dim, 0), (0, bright, 0), (0, brightest, 0)],
    "CYAN": [(0, dim, 150), (0, bright, bright), (0, brightest, brightest)],
    "BLUE": [(0, 0, dim), (0, 0, bright), (0, 0, brightest)],
    "PURPLE": [(dim, 0, dim), (bright, 0, bright), (brightest, 0, brightest)],
}


def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(text, x, y, width, height, inactive_color, active_color, click_color=None, label_color=black,
           font_type="freesansbold.ttf", font_size=20, action=None):
    if click_color is None:
        click_color = active_color

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))

        # print(click)
        if click[0] == 1:
            if action != None:
                action()
            else:
                pygame.draw.rect(gameDisplay, click_color,
                                 (x, y, width, height))
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    smallText = pygame.font.SysFont('comicsansms', 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = (x+(width/2), y+(height/2))
    gameDisplay.blit(textSurf, textRect)


def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def node_button_attack_from(node, radius, width=0, font_color=white,
                            font_type='roboto', font_size=30, action=None, curr_player=None):
    global selected_node_attack_from

    troops = node.get_troops()
    # For some reason, when resizing, one needs to keep the old node locations
    # when placing nodes BUT new locations when calculating distances, which
    # is reflected in the variables (x, y) - "old", and (x_dist, y_dist) -
    # "new", resized.
    x, y = node.get_location()
    x_dist, y_dist = locations[node.get_name()]
    # Inactive color, active color, click color.
    ic, ac, cc = colors[node.get_owner().name]

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Node already selected.
    if selected_node_attack_from is not None:
        if selected_node_attack_from == node:
            pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
            return
        else:
            pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)
            return

    # No node is currently selected.
    # Could potentially choose the node.
    if node.get_owner() == curr_player.get_color() and troops > 1:
        # Mouse hovered over a node that could potentially be selected.
        if distance(mouse, (x_dist, y_dist)) <= radius+width:
            # Node selected.
            if click[0]:
                selected_node_attack_from = node
            pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
        else:
            pygame.draw.circle(gameDisplay, ac, (x, y), radius, width)
    # Node doesn't belong to the player or has 1 troop.
    else:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)

    # Display troops.
    smallText = pygame.font.SysFont(font_type, font_size)
    textSurf, textRect = text_objects(str(troops), smallText, font_color)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)


def node_button_attack_to(node,  radius, width=0, font_color=white,
                          font_type='roboto', font_size=30, action=None, curr_player=None):
    global selected_node_attack_from
    global selected_node_attack_to
    global blitz_res

    # For some reason, when resizing, one needs to keep the old node locations
    # when placing nodes BUT new locations when calculating distances, which
    # is reflected in the variables (x, y) - "old", and (x_dist, y_dist) -
    # "new", resized.
    x, y = node.get_location()
    x_dist, y_dist = locations[node.get_name()]
    # Inactive color, active color, click color.
    ic, ac, cc = colors[node.get_owner().name]

    # Needs to choose a node to attack from again.
    if selected_node_attack_from is None:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)
        return
    # Node to attack has already been picked.
    elif selected_node_attack_to is not None and selected_node_attack_to != node:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)
        return

    selected_node_owner = selected_node_attack_from.get_owner()

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Current node is selected.
    if selected_node_attack_from == node:
        # Code below might be confusing but it's necessary for bug-free run.
        # If left-click is made AND it is not on the one of the possible options
        # reassign selected_node_attack_from and go back to selecting the node
        # to attack from. Otherwise, return before reassigning the global
        # variable and let the other nodes conduct the attack and record
        # changes.
        if click[0] and distance(mouse, (x_dist, y_dist)) > radius+width:
            for n in node.attack_options():
                x_dist_n, y_dist_n = locations[n.get_name()]
                if distance(mouse, (x_dist_n, y_dist_n)) <= radius+width:
                    return
            selected_node_attack_from = None
        # Still selected but no click.
        else:
            pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
    # Node could be attacked from a selected node.
    elif node in selected_node_attack_from.get_neighbors() and node.get_owner() != selected_node_owner:
        # Mouse is hovered above the node.
        if distance(mouse, (x_dist, y_dist)) <= radius+width:
            # Node is selected to be attacked.
            if click[0]:
                selected_node_attack_to = node
                blitz_res = blitz_attack(selected_node_attack_from, node)
                pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)
            else:
                pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
        # Mouse is not above the node.
        else:
            pygame.draw.circle(gameDisplay, ac, (x, y), radius, width)
    # Node cannot be attacked from a selected node.
    else:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)

    # Display troops.
    smallText = pygame.font.SysFont(font_type, font_size)
    textSurf, textRect = text_objects(
        str(node.get_troops()), smallText, font_color)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)


def current_player_display(curr_player, loc):
    left, y = loc
    curr_color = curr_player.get_color()

    display_colors = colors[curr_color.name]
    largeText = pygame.font.SysFont("consolas", 30, bold=False)
    TextSurface, TextRect = text_objects(
        curr_color.name, largeText, display_colors[2])
    TextRect.left = left
    TextRect.y = y

    gameDisplay.blit(TextSurface, TextRect)


def display_nodes_attack_from(node_lst, curr_player):
    for node in node_lst:
        node_button_attack_from(node, 20, width=5, font_color=white,
                                action=None, curr_player=curr_player)


def display_nodes_attack_to(node_lst, curr_player):
    for node in node_lst:
        node_button_attack_to(node, 20, width=5, font_color=white,
                              action=None, curr_player=curr_player)


def print_console(text):
    consoleText = pygame.font.SysFont("consolas", 30, bold=False)
    textSurf, textRect = text_objects(text, consoleText, white)
    textRect.left = 10
    textRect.y = 865

    gameDisplay.blit(textSurf, textRect)


def game_quit():
    pygame.quit()
    quit()


locations = {
    "Afghanistan": (776, 370),
    "Alaska": (79, 210),
    "Alberta": (198, 255),
    "Argentina": (283, 725),
    "Brazil": (367, 609),
    "Central America": (215, 415),
    "China": (926, 420),
    "Congo": (591, 642),
    "East Africa": (673, 600),
    "Eastern Australia": (1011, 682),
    "Eastern United States": (290, 354),
    "Egypt": (603, 492),
    "Great Britain": (507, 303),
    "Greenland": (457, 176),
    "Iceland": (506, 217),
    "India": (822, 512),
    "Indonesia": (944, 602),
    "Irkutsk": (951, 286),
    "Japan": (1048, 364),
    "Kamchatka": (1115, 213),
    "Madagascar": (691, 723),
    "Middle East": (696, 500),
    "Mongolia": (980, 347),
    "New Guinea": (1074, 597),
    "North Africa": (521, 551),
    "Northern Europe": (593, 331),
    "Northwest Territory": (245, 210),
    "Ontario": (275, 260),
    "Peru": (249, 613),
    "Quebec": (370, 256),
    "Russia": (686, 282),
    "Scandinavia": (563, 234),
    "Siam": (912, 500),
    "Siberia": (880, 230),
    "South Africa": (582, 762),
    "Southern Europe": (589, 392),
    "Ural": (808, 268),
    "Venezuela": (251, 529),
    "Western Australia": (946, 706),
    "Western Europe": (505, 395),
    "Western United States": (200, 360),
    "Yakutsk": (993, 208)
}


def rescale_locations(w, h):
    '''Rescale for the current resolution (the original locations are for 1200X900).'''
    print(w, h)
    for loc in locations:
        coords = locations[loc]
        x = int(coords[0] * w/1200)
        y = int(coords[1] * h/900)
        locations[loc] = (x, y)
    # for node in all_nodes:
    #     x, y = node.get_location()
    #     x_new = int(x*w/1200)
    #     y_new = int(y*h/900)
    #     node.set_location(((x * w/1200, y * h/900)))


for node in all_nodes:
    node.set_location(locations[node.get_name()])


def blitz_attack(from_node, to_node):
    '''Conducts blitz attack between the two nodes and changes the results.
    Returns a boolean representing whether attack was successful or not.

    Preconditions: from_node.get_troops() > 1 and to_node.get_troops() > 0;
        the nodes have two different owners.'''

    blitz_res = blitz(from_node.get_troops(), to_node.get_troops())

    if blitz_res[0] == 1:
        print("Attack unsuccessful! You now have 1 troop in " + from_node.get_name() + ". The " + str(to_node.get_owner()) +
              " player has " + str(blitz_res[1]) + " troops in " + to_node.get_name())
        from_node.set_troops(1)
        to_node.set_troops(blitz_res[1])
        return False
    elif blitz_res[1] == 0:
        print("\nAttack successful!")
        from_node.set_troops(1)
        to_node.set_troops(blitz_res[0]-1)
        to_node.set_owner(from_node.get_owner())
        print("\nYou now have 1 troop in %s and %i troops in %s." % (
            from_node.get_name(), to_node.get_troops(), to_node.get_name()))
        return True
    else:
        raise ValueError("Wrong results for blitz: (%i, %i)" % blitz_res)


blitz_res = None
selected_node_attack_from = None
selected_node_attack_to = None


def attack_phase():
    global blitz_res
    global selected_node_attack_from
    global selected_node_attack_to

    blitz_res = None
    selected_node_attack_from = None
    selected_node_attack_to = None

    curr_player = order.pop(0)
    order.append(curr_player)
    curr_color = curr_player.get_color()
    phase_over = False

    while not phase_over:

        # Selecting a node to attack from.
        while selected_node_attack_from is None:
            gameDisplay.blit(bgImg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()
                if event.type == pygame.VIDEORESIZE:
                    rescale_locations(event.w, event.h)
                    # print(locations)

            print_console("%s Player: pick a territory to attack from. The territory should have at least 1 troop." %
                          curr_color)
            display_nodes_attack_from(all_nodes, curr_player)
            # current_player_display(curr_player, (10, 865))

            pygame.display.update()
            clock.tick(15)

        # Selecting a node to attack.
        while selected_node_attack_to is None:
            # Node to attack from was unselected. Return to the first while-loop.
            if selected_node_attack_from is None:
                break

            gameDisplay.blit(bgImg, (0, 0))

            display_nodes_attack_to(all_nodes, curr_player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()
                if event.type == pygame.VIDEORESIZE:
                    rescale_locations(event.w, event.h)
                    # print(locations)

            # current_player_display(curr_player, (10, 865))

            if blitz_res is not None:
                assert selected_node_attack_from is not None
                assert selected_node_attack_to is not None
                phase_over = True
                # Code below not working due to a bug in time.sleep() for Mac.
                # node_to = selected_node_attack_to
                # if blitz_res:
                #     print_console("%s Player: the attack was successful! You now have 1 troop in %s and %i troops in %s." %
                #                   (curr_color, selected_node_attack_from.get_name(), node_to.get_troops(), node_to.get_name()))
                #     time.sleep(2)
                # else:
                #     print_console("%s Player: the attack was unsuccessful! You now have 1 troop in %s. %s Player has %i troops in %s." %
                #                   (curr_color, selected_node_attack_from.get_name(), node_to.get_owner(), node_to.get_troops(), node_to.get_name()))
                #     time.sleep(2)
            else:
                print_console(
                    "%s Player: choose an enemy territory to attack." % curr_color)

            pygame.display.update()
            clock.tick(15)


while True:
    attack_phase()
