"""
===================
BBC Technical Test
===================

Author: GilEstelsBeams
Date: 6/2/2019

"""

import pygame
import random

# PARAMETERS TO SET (can be set while running the programme)

H = 50  # Height of the grid in number of cells
L = 50  # Length of the grid in number of cells
torus = False  # option to "delete" the borders

# The starting point of the game:
# 'drawn':player chooses before starting,
# 'number': then define 'Prob', with Prob=1/prob(starting cell is alive)
Start = 'drawn'
Prob = 4

Speed = 10  # number of iterations per second
squares = 16  # size of the cell's side, between 8 and 64, needs to be even

Black = (0, 0, 0)
White = (255, 255, 255)
Blue = (16, 208, 234)
Yellow = (249, 252, 52)

Gamebackground = White
Alivecells = Black
Pausedbackground = Yellow

run = False  # whether or not it starts running by itself or wait for the space key to be pushed

Background = Pausedbackground


# FUNCTIONS AND CLASS USED


class Cell:
    def __init__(self, location, alive=True):

        self.state = alive
        self.location = location

    def paint(self):

        if self.state:
            self.colour = Alivecells
        else:
            self.colour = Background


def set_parameters(x, y, w, p, q):  # asks if the user wants to manually change the parameters
    print('If you would like to change the parameters, write Y. Otherwise press Enter.')
    par = input('Answer')
    if par == 'Y':
        print('Height of the grid in number of cells')
        x = int(input('Answer:'))
        print('Length of the grid in number of cells')
        y = int(input('Answer:'))

        print("Choose the starting state of the grid:drawn or number")
        w = input('Answer:')
        if w == 'number':
            print('Choose a positive N, with N=1/Prob(A starting cell is alive)')
            p = int(input('Answer:'))

        print('Size of each cell, between 8 and 64 advised, needs to be positive and even')
        q = int(input('Answer:'))

    return [x, y, w, p, q]


def initiate(S, H1, L1, P, ri):  # Creates the list that contains our data
    cell_l = [[] for i in range(H1)]

    for h in range(H1):

        for l in range(L1):
            x1 = int(l * 2 * ri + ri)
            x2 = int(h * 2 * ri + ri)

            if S == 'drawn': life = False
            if S == 'number':
                lifeb = random.choices([True, False], [1 / P, 1 - 1 / P])
                life = lifeb[0]

            startcell = Cell([x1, x2], life)
            cell_l[h].append(startcell)
            startcell.paint()
            pygame.draw.circle(screen, startcell.colour, startcell.location, int(ri))
    return cell_l


def count_neighbours(h, l, c, cell_list):  # counts the neighbouring cells
    n = 0
    for i in range(max(h - 1, 0), min(h + 2, H)):
        for j in range(max(l - 1, 0), min(L, l + 2)):
            if i != h or j != l:
                if cell_list[i][j].state:
                    n = n + 1

    if torus:  # Special case where there are no real borders
        if h == 0:
            i = H - 1
            for j in range(max(l - 1, 0), min(L, l + 2)):
                if cell_list[i][j].state:
                    n = n + 1
        if l == 0:
            j = L - 1
            for i in range(max(h - 1, 0), min(h + 2, H)):
                if cell_list[i][j].state:
                    n = n + 1
        if h == H - 1:
            i = 0
            for j in range(max(l - 1, 0), min(L, l + 2)):
                if cell_list[i][j].state:
                    n = n + 1

        if l == L - 1:
            j = 0
            for i in range(max(h - 1, 0), min(h + 2, H)):
                if cell_list[i][j].state:
                    n = n + 1

    return n


def life_or_death(n, s):  # decides of the future of the cell
    v = False
    if s and n == 2:
        v = True

    if n == 3:
        v = True
    return v


# MAIN FUNCTION
print('')
print('Hello! Welcome to the Game of Life.')
print('')
print('First a few rules:')
print('')
print(
    'Use the space key for starting and pausing the game. The backspace is for restarting the board. Press t to switch the torus mode on or off.')
print('Use the Up and Down arrow for increasing or decreasing the speed respectively.')
print('Left click for making a cell alive, right click for killing it')
print('To stop the game just press escape or close the window.')
print('')
print('Enjoy!')
print('')

[H, L, Start, Prob, squares] = set_parameters(H, L, Start, Prob, squares)
print('Your game is ready to start now, the window is opened')
pygame.init()

# We first create the pygame window
r = squares / 2
a = squares * H
b = squares * L
size = (int(a), int(b))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Game of Life")

carryOn = True

clock = pygame.time.Clock()
screen.fill(Background)

# Then we create the 2D list with all the cells

cell_list = initiate(Start, H, L, Prob, r)

# We create a copy of the cell_list so that it contains the future values
cell_list2 = cell_list

while carryOn:

    if not run:
        Background = Pausedbackground
    else:
        Background = Gamebackground

    clock.tick(Speed)

    # We take into account any action taken by the player with the keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = not run
            if event.key == pygame.K_BACKSPACE:
                cell_list = initiate(Start, H, L, Prob, r)
                cell_list2 = cell_list
            if event.key == pygame.K_t:
                torus = not torus
            if event.key == pygame.K_UP:
                Speed = Speed + 0.5
            if event.key == pygame.K_DOWN:
                Speed = Speed - 0.5
            if event.key == pygame.K_ESCAPE:
                carryOn = False

    clicked = pygame.mouse.get_pressed()
    locm = pygame.mouse.get_pos()

    screen.fill(Background)

    # Now we deal with the cells

    for h in range(H):
        for l in range(L):

            c = cell_list[h][l]

            cell_list2[h][l] = Cell(c.location, c.state)
            c2 = cell_list2[h][l]

            n = count_neighbours(h, l, c, cell_list)

            if run:
                c2.state = life_or_death(n, c.state)  # The function that updates c2 with the next states

            # We take care of the clicks from the player

            loc = c.location
            if clicked[0]:

                if (loc[0] - r) < locm[0] < loc[0] + r and loc[1] - r < locm[1] < loc[1] + r:
                    c2.state = True

            if clicked[2]:
                if (loc[0] - r) < locm[0] < loc[0] + r and loc[1] - r < locm[1] < loc[1] + r:
                    c2.state = False

            c.paint()
            pygame.draw.circle(screen, c.colour, c.location, int(r))

    # Now we replace the list with present alive values with the values from the next round
    cell_list = cell_list2
    pygame.display.flip()

pygame.quit()
