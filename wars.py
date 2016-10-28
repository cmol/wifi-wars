#!/usr/bin/env python3

import pygame,sys
from pygame.locals import *

pygame.init()

from wars.block import Block
from wars.device import Device


# We'll run (target) at 30FPS for now
FPS = 30
fpsClock = pygame.time.Clock()

# Initialise general stuff
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("WiFi Wars")

# Define constants for later use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLS  = {
        'RTS':  (67,124,144),
        'CTS':  (37,89,87),
        'DATA': (238,235,211),
        'ACK':  (169,135,67),
        'DIFS': (247,197,72),
        'SIFS': (255,140,0)
        }


# List of AP's
aps = []

# List of stations
stations = []

# TODO: Some kind of initialiser that actually makes some descitions based in
#   the users input are made. This includes creating STs and APs.

def draw_window():
    pass

def draw_lines():
    for ap in aps:
        ap.draw(DISPLAYSURF)
    for st in stations:
        st.draw(DISPLAYSURF)

def move_lines():
    for ap in aps:
        ap.move_blocks(1)
    for st in stations:
        st.move_blocks(1)

def make_block(block):
    if block == 'RTS':
        return Block(size=60,end=400,text="RTS",color=COLS['RTS'],text_color=BLACK)
    elif block == 'CTS':
        return Block(size=60,end=400,text="CTS",color=COLS['CTS'],text_color=BLACK)
    elif block == 'DATA':
        return Block(size=120,end=400,text="DATA",color=COLS['DATA'],text_color=BLACK)
    elif block == 'ACK':
        return Block(size=30,end=400,text="ACK",color=COLS['ACK'],text_color=BLACK)

# Main loop
if __name__ == "__main__":

    # Default test code
    ap = Device("AP",0)
    ap.add_block(make_block('DATA'))
    aps = [ap]

    st = Device("ST",1)
    st.add_block(make_block('ACK'))
    stations = [st]

    while True:
        DISPLAYSURF.fill(WHITE)

        # Draw main window features along with STs and APs
        draw_window()

        # Draw tranmission boxes
        draw_lines()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

        # Move blocks
        move_lines()

        # Tick clock
        fpsClock.tick(FPS)
