#!/usr/bin/env python3

import pygame,sys
from pygame.locals import *

from wars.block import Block

pygame.init()

# We'll run (target) at 30FPS for now
FPS = 30
fpsClock = pygame.time.Clock()

# Initialise general stuff
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("WiFi Wars")

# Define constants for later use
WHITE = (255, 255, 255)

# List of blocks that needs to be drawn
blocks = []

# List of AP's
aps = []

# List of stations
stations = []

# TODO: Some kind of initialiser that actually makes some descitions based in
#   the users input are made. This includes creating STs and APs.

# Main loop
while True:
    DISPLAYSURF.fill(WHITE)

    # Draw main window features along with STs and APs
    draw_window()

    # Draw tranmission boxes
    draw_boxes()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
