#!/usr/bin/env python3

import pygame,sys
from pygame.locals import *

pygame.init()

from wars.block import Block
from wars.device import Device


# We'll run (target) at 30FPS for now
FPS = 30
fpsClock = pygame.time.Clock()
SCREEN_SIZE = (400, 300)
speed = 2

# Initialise general stuff
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
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

SIZES = {
        'RTS':   60,
        'CTS':   60,
        'DATA': 120,
        'ACK':   60,
        'DIFS':  60,
        'SIFS':  30
        }

FLOW  = [
        ('DIFS', 0),
        ('RTS' , 0),
        ('SIFS', 1),
        ('CTS' , 1),
        ('SIFS', 0),
        ('DATA', 0),
        ('SIFS', 1),
        ('ACK' , 1)
        ]

# Basically a state machine over the flow
flow_index = 0

# Devices
devices = []

# Blocks
blocks  = []

def draw_window():
    pass

def draw_lines():
    for dev in devices:
        dev.draw(DISPLAYSURF)

def move_lines():
    for dev in devices:
        dev.move_blocks(speed)

def make_block(block, start, text=None):
    if text == None:
        text = block

    return Block(size=SIZES[block],start=start,text=text,color=COLS[block],text_color=BLACK)

def reset():
    flow_index = 0
    del blocks[:]
    for dev in devices:
        dev.reset()

# Main loop
if __name__ == "__main__":

    # Define devices
    devices.append(Device("AP",0))
    devices.append(Device("ST",1))

    while True:
        # No loops!
        flow_index = flow_index % len(FLOW)

        if blocks and blocks[0].pos_x == 0:
            reset()

        # Do we need to add a block
        if (not blocks) or blocks[-1].right_edge() < SCREEN_SIZE[0]:
            start = blocks[-1].right_edge() if blocks else SCREEN_SIZE[0]

            blocks.append(make_block(FLOW[flow_index][0], start))
            devices[FLOW[flow_index][1]].add_block(blocks[-1])
            flow_index = flow_index + 1

        # BELOW THIS, THINGS ARE RELATED TO DRAWING
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
