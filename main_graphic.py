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
blue = (0, 0, 255)
brown = (139, 69, 19)

brighter_red = (220, 0, 0)
brighter_green = (0, 220, 0)
brightest_red = (255, 0, 0)
brightest_green = (0, 255, 0)

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

def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()
        if event.type == pygame.VIDEORESIZE:
            rescale_locations(event.w, event.h)

def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def load_img(path):
    img_unscaled = pygame.image.load(path)
    x, y = img_unscaled.get_rect().size
    img = pygame.transform.scale(
        img_unscaled, (int(x*display_width/1600), int(y*display_height/1200)))
    return img


def button_textless_rect(x, y, inactive_img, active_img, action=None, alternative_action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    width, height = inactive_img.get_rect().size

    if x-width/2 < mouse[0] < x+width/2 and y-height/2 < mouse[1] < y+height/2:
        # print('if')
        gameDisplay.blit(active_img, (x-width/2, y-height/2))
        if click[0] == 1:
            if action is not None:
                action() 
    # elif click[0] == 1 and alternative_action is not None:
    #     alternative_action()
    else:
        # print('else')
        gameDisplay.blit(inactive_img, (x-width/2, y-height/2))

    # pygame.display.update()
    # clock.tick(15)


def button_textless_circular(x, y, inactive_img, active_img, action=None, alternative_action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    width, height = inactive_img.get_rect().size
    radius = width/2

    if distance(mouse, (x, y)) <= radius:
        # print('if')        
        gameDisplay.blit(active_img, (x-width/2,y-height/2))
        
        if click[0] == 1:
            if action is not None:
                action()
    # elif click[0] == 1 and alternative_action is not None:
    #     alternative_action()
    else:
        # print('else')
        width, height = inactive_img.get_rect().size
        gameDisplay.blit(inactive_img, (x-width/2,y-height/2))

    # pygame.display.update()
    # clock.tick(15)


def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def node_button_deploy(node, radius, width=0, font_color=white,
                       font_type='roboto', font_size=30, curr_player=None):
    global selected_node_deploy
    global deploy_in_progress

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
    if selected_node_deploy == node:
        pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
        if not deploy_in_progress and click[0] and distance(mouse, (x_dist, y_dist)) > radius+width:
            selected_node_deploy = None
    elif selected_node_deploy is not None:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)

    # No node yet selected and this node is belongs to the player.
    if node.get_owner() == curr_player.get_color():
        # Mouse hovered over the node.
        if distance(mouse, (x_dist, y_dist)) <= radius+width:
            # Node selected.
            if click[0]:
                selected_node_deploy = node
                deploy_in_progress = True
            pygame.draw.circle(gameDisplay, cc, (x, y), radius, width)
        else:
            pygame.draw.circle(gameDisplay, ac, (x, y), radius, width)
    # This node can't be selected since it doesn't belong to the player.
    else:
        pygame.draw.circle(gameDisplay, ic, (x, y), radius, width)

    # Display troops.
    smallText = pygame.font.SysFont(font_type, font_size)
    textSurf, textRect = text_objects(
        str(node.get_troops()), smallText, font_color)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)


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


def num_displayed_increase():
    '''Helper function for display_numbers().'''
    global num_displayed
    num_displayed += 1


def num_displayed_decrease():
    '''Helper function for display_numbers().'''
    global num_displayed
    num_displayed -= 1


def deselect_deploy_node():
    '''Helper function for display_numbers().'''
    global selected_node_deploy
    global deploy_in_progress
    selected_node_deploy = None
    deploy_in_progress = False


def place_troops_deploy():
    '''Helper function for display_numbers().'''
    global num_displayed
    global selected_node_deploy
    global deploy_in_progress

    assert selected_node_deploy is not None
    assert deploy_in_progress

    selected_node_deploy.add_troops(num_displayed)
    curr_player.subtract_troops(num_displayed)

    selected_node_deploy = None
    deploy_in_progress = False

def go_back_deploy():
    '''Helper function for display_numbers().'''
    global deploy_in_progress
    global selected_node_deploy

    deploy_in_progress = False
    selected_node_deploy = None

def occupy_territory():
    '''Helper function for display_numbers().'''
    global num_displayed
    global selected_node_attack_from
    global selected_node_attack_to
    global territory_occupied

    assert selected_node_attack_to is not None
    assert not territory_occupied

    total_troops = selected_node_attack_from.get_troops() + selected_node_attack_to.get_troops()

    selected_node_attack_to.set_troops(num_displayed)
    selected_node_attack_from.set_troops(total_troops-num_displayed)

    territory_occupied = True

# def go_back_occupy():
#     '''Helper function for display_numbers().'''
#     global territories
#     global selected_node_deploy

#     deploy_in_progress = False
#     selected_node_deploy = None

def finish_attack_phase():
    global attack_phase_over
    assert not attack_phase_over
    attack_phase_over = True


def display_numbers(max_num, min_num=1, tick_action=None, cross_action=None, running_condition=None):
    ''' Displays a numerical window to choose the number of troops with the 
    two arrows. Numbers go from 1 to [max_num] and then, if increased, cycle 
    back to one; similarly, if user presses the "smaller" button when the
    number displayed is 1, the next number is [max_num].
    In case if the tick is clicked, does [tick_action]. In case if the cross 
    is clicked, does [cross_action]. At every frame, checks for 
    [running_condition] and returns  if it's False.

    Preconditions: [max_num] is int; [tick_action], [cross_action] are functions;
    [running_condition] is bool.'''
    global num_displayed


    number_bg_img = load_img("Number_bg.png")
    right_img = load_img("Right.png")
    right_active_img = load_img("Right_active.png")
    left_img = load_img("Left.png")
    left_active_img = load_img("Left_active.png")
    tick_img = load_img("Tick.png")
    tick_active_img = load_img("Tick_active.png")
    cross_img = load_img("Cross.png")
    cross_active_img = load_img("Cross_active.png")

    # If player clicks outside of the table, one has to select a node again.
    button_textless_rect(0.125*display_width, display_height/9,
                    number_bg_img, number_bg_img, alternative_action=deselect_deploy_node)
    button_textless_rect(0.17*display_width, display_height/9,
                    right_img, right_active_img, action=num_displayed_increase)
    button_textless_rect(0.08*display_width, display_height/9,
                    left_img, left_active_img, action=num_displayed_decrease)
    button_textless_circular(0.22*display_width, display_height/9,
                    tick_img, tick_active_img, action=tick_action)
    button_textless_circular(0.03*display_width, display_height/9,
                    cross_img, cross_active_img, action=cross_action)
    
    if not running_condition:
        return

    # Check if the number went out of bounds.
    if num_displayed > max_num:
        num_displayed = min_num
    elif num_displayed < min_num:
        num_displayed = max_num
    # Display the number.
    numberText = pygame.font.SysFont("consolas", 30, bold=True)
    textSurf, textRect = text_objects(str(num_displayed), numberText, brown)
    textRect.center = (0.125*display_width, display_height/9)

    event_loop()

    gameDisplay.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(15)
    


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


def display_nodes_deploy(node_lst, curr_player):
    for node in node_lst:
        node_button_deploy(node, 20, width=5,
                           font_color=white, curr_player=curr_player)


def display_nodes_attack_from(node_lst, curr_player):
    for node in node_lst:
        node_button_attack_from(node, 20, width=5, font_color=white,
                                action=None, curr_player=curr_player)


def display_nodes_attack_to(node_lst, curr_player):
    for node in node_lst:
        node_button_attack_to(node, 20, width=5, font_color=white,
                              action=None, curr_player=curr_player)


def print_console(text):
    consoleText = pygame.font.SysFont("consolas", 23, bold=True)
    textSurf, textRect = text_objects(text, consoleText, white)
    textRect.left = 10
    textRect.y = 865

    gameDisplay.blit(textSurf, textRect)


def print_phase(phase):
    phaseText = pygame.font.SysFont("trebuchet", 60, bold=False)
    textSurf, textRect = text_objects(phase, phaseText, white)
    textRect.center = ((0.5*display_width, display_height/36))

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


def darken_screen():
    dark = pygame.Surface(
        (bgImg.get_width(), bgImg.get_height()), flags=pygame.SRCALPHA)
    dark.fill((10, 10, 10, 0))
    for _ in range(3):
        bgImg.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


def lighten_screen():
    dark = pygame.Surface(
        (bgImg.get_width(), bgImg.get_height()), flags=pygame.SRCALPHA)
    dark.fill((10, 10, 10, 0))
    for _ in range(3):
        bgImg.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)


def blitz_attack(from_node, to_node):
    '''Conducts blitz attack between the two nodes and changes the results.
    Returns a boolean representing whether attack was successful or not.
    In case of a successful attack, moves all possible troops into a new
    territory; however, this is done purely for bookkeeping purposes when 
    letting the player choose how many troops to actually move in.

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
        # print("\nYou now have 1 troop in %s and %i troops in %s." % (
        #     from_node.get_name(), to_node.get_troops(), to_node.get_name()))
        return True
    else:
        raise ValueError("Wrong results for blitz: (%i, %i)" % blitz_res)


num_displayed = None
selected_node_deploy = None
# Represents if player is currently choosing the number of troops to be deployed.
deploy_in_progress = False


def deploy_phase(curr_player):
    global selected_node_deploy
    global deploy_in_progress
    global num_displayed

    deploy_in_progress = False

    curr_color = curr_player.get_color()
    troops_gained, _, _ = calculate_troops_gained(curr_color, continents, True)
    curr_player.add_troops(troops_gained)

    while curr_player.get_troops() > 0:

        # Selecting node to put troops to.
        while selected_node_deploy is None:

            gameDisplay.blit(bgImg, (0, 0))
            print_phase("DEPLOY")

            event_loop()

            if curr_player.get_troops() == 1:
                print_console(
                    "%s Player: Choose where to deploy troops. You have %i more troop." % (curr_color, curr_player.get_troops()))
            else:
                print_console(
                    "%s Player: Choose where to deploy troops. You have %i more troops." % (curr_color, curr_player.get_troops()))
            display_nodes_deploy(all_nodes, curr_player)

            pygame.display.update()
            clock.tick(15)

        # Selecting the number of troops to put.
        darken_screen()
        num_displayed = curr_player.get_troops()
        while deploy_in_progress:

            gameDisplay.blit(bgImg, (0, 0))
            print_console("%s Player: Choose how many troops to deploy in %s." % (
                curr_color, selected_node_deploy.get_name()))
            print_phase("DEPLOY")

            event_loop()

            display_nodes_deploy(all_nodes, curr_player)
            display_numbers(max_num=curr_player.get_troops(), min_num=1, tick_action=place_troops_deploy, cross_action=go_back_deploy, running_condition=deploy_in_progress)

            # tick_img = pygame.image.load("Tick.png")
            # tick_active_img = pygame.image.load("Tick_active.png")

            # button_textless(int(0.1*display_width), int(display_height/8),
            #                 tick_img, tick_active_img, action=place_troops)

            pygame.display.update()
            pygame.event.get()
            clock.tick(15)
        lighten_screen()


blitz_res = None
selected_node_attack_from = None
selected_node_attack_to = None
territory_occupied = None
attack_phase_over = None


def attack_phase(curr_player):
    global blitz_res
    global selected_node_attack_from
    global selected_node_attack_to
    global territory_occupied
    global attack_phase_over

    blitz_res = None
    selected_node_attack_from = None
    selected_node_attack_to = None
    territory_occupied = False
    attack_phase_over = False

    curr_color = curr_player.get_color()
    skip_img = load_img("Skip.png")
    skip_active_img = load_img("Skip_active.png")

    while not attack_phase_over:


        # Selecting node to attack from.
        while selected_node_attack_from is None:
            
            gameDisplay.blit(bgImg, (0, 0))
            print_phase("ATTACK")
            
            # Finish phase.
            button_textless_rect(0.825*display_width, display_height/10, skip_img, skip_active_img, action=finish_attack_phase)
            if attack_phase_over:
                break

            event_loop()

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
            print_phase("ATTACK")
            display_nodes_attack_to(all_nodes, curr_player)
            print_console("%s Player: Choose an enemy territory to attack." % curr_color)

            # Finish phase.
            button_textless_rect(0.825*display_width, display_height/10, skip_img, skip_active_img, action=finish_attack_phase)
            if attack_phase_over:
                break

            event_loop()

            # current_player_display(curr_player, (10, 865))

            # Attack successful. Let player choose how many troops to move.
            if blitz_res:
                darken_screen()
                while not territory_occupied:

                    gameDisplay.blit(bgImg, (0, 0))
                    print_phase("ATTACK")
                    display_nodes_attack_to(all_nodes, curr_player)

                    event_loop()
                    
                    from_node = selected_node_attack_from
                    to_node = selected_node_attack_to
                    
                    print_console("%s Player: Attack successful! Move up to %i troops in %s." % (curr_color, to_node.get_troops(), to_node.get_name()))
                    # Currently: 1 troop in [from_node] and the remaining troops in [to_node]. Thus, can move up to [to_node.get_troops()] troops
                    # into [to_node].
                    display_numbers(max_num=to_node.get_troops(), min_num=3, tick_action=occupy_territory, cross_action=None, running_condition=not territory_occupied)

                    pygame.display.update()
                    clock.tick(15)
                lighten_screen()


            # Reset global variables to let player conduct another attack.
            if blitz_res is not None:
                assert selected_node_attack_from is not None
                assert selected_node_attack_to is not None
                blitz_res = None
                selected_node_attack_from = None
                selected_node_attack_to = None

                # attack_phase_over = True
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
            # else:

            pygame.display.update()
            clock.tick(15)


while True:
    curr_player = order.pop(0)
    order.append(curr_player)
    # num_displayed = curr_player.get_troops()
    # i = 0
    # while i < 100:
    #     tick_img = pygame.image.load("Tick.png").convert()
    #     tick_img = pygame.transform.scale(tick_img, (display_width, display_height))
    #     gameDisplay.blit(bgImg, (0, 0))

    #     pygame.display.update()
    #     clock.tick(15)
    #     i += 1
    deploy_phase(curr_player)
    attack_phase(curr_player)