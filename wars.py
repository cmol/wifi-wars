#!/usr/bin/env python3

import pygame,sys
from pygame.locals import *
from random import randint

pygame.init()

from wars.block import Block
from wars.device import Device

# We'll run (target) at 30FPS for now
FPS = 30
fpsClock = pygame.time.Clock()
SCREEN_SIZE = (892, 595)
speed = 1

# Initialise general stuff
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.display.set_caption("WiFi Wars")

# Define constants for later use
FONT  = pygame.font.Font(None, 84)
BG    = pygame.image.load('img/wars.png')
BGREC = BG.get_rect()
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
        'RTS':  120,
        'CTS':  120,
        'DATA': 240,
        'ACK':  120,
        'DIFS': 120,
        'SIFS':  60
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

KEYS = {
      K_a: "a",
      K_b: "b",
      K_c: "c",
      K_d: "d",
      K_e: "e",
      K_f: "f",
      K_g: "g",
      K_h: "h",
      K_i: "i",
      K_j: "j",
      K_k: "k",
      K_l: "l",
      K_m: "m",
      K_n: "n",
      K_o: "o",
      K_p: "p",
      K_q: "q",
      K_r: "r",
      K_s: "s",
      K_t: "t",
      K_u: "u",
      K_v: "v",
      K_w: "w",
      K_x: "x",
      K_y: "y",
      K_z: "z",
      K_0: "0",
      K_1: "1",
      K_2: "2",
      K_3: "3",
      K_4: "4",
      K_5: "5",
      K_6: "6",
      K_7: "7",
      K_8: "8",
      K_9: "9"
      }

# Basically a state machine over the flow
flow_index = 0

# Devices
devices = []

# Blocks
blocks  = []

# Typing housekeeping
typing  = []
delete_with_next = False

# Scoring system
score           = 0
POINT_FOR_BLOCK = 1
POINT_FOR_SEQ   = 30
PENALTY         = 15
UP_SPEED_AT     = 250

def draw_scores():
    global speed, score
    text = FONT.render(str(int(speed)), True, WHITE)
    textpos = text.get_rect()
    textpos.right   = 310
    textpos.centery = 527
    DISPLAYSURF.blit(text,textpos)
    text = FONT.render(str(int(score)), True, WHITE)
    textpos = text.get_rect()
    textpos.right   = 810
    textpos.centery = 527
    DISPLAYSURF.blit(text,textpos)

def draw_lines():
    global devices
    for dev in devices:
        dev.draw(DISPLAYSURF)

def move_lines():
    global devices, blocks
    for dev in devices:
        dev.move_blocks(speed)

    for block in blocks:
        if block.right_edge() < -5:
            blocks.remove(block)

def make_block(block, start, text=None):
    if text == None:
        text = block
    return Block(size=SIZES[block],start=start,text=text,color=COLS[block],text_color=BLACK)

def reset():
    global flow_index, blocks, typing, devices
    flow_index = 0
    del blocks[:]
    del typing[:]
    for dev in devices:
        dev.reset()

def add_typing(block):
    global typing
    typing.append(list(block.box_text))

def key_input(char):
    global score, blocks, typing, delete_with_next
    if char.upper() == typing[0][0].upper():
        score = score + POINT_FOR_BLOCK
        del typing[0][0]
        if not typing[0]:
            del typing[0]
            blocks[0].clear()
            score = score + POINT_FOR_SEQ

            # If the block is still outside the screen, do not delete it yet.
            if blocks[0].right_edge() > SCREEN_SIZE[0]:
                delete_with_next = True
            else:
                blocks.remove(blocks[0])
    else:
        score = score - PENALTY
        reset()

# Main loop
if __name__ == "__main__":

    # Define devices
    devices.append(Device("AP",0))
    devices.append(Device("ST",1))

    while True:
        # No loops!
        flow_index = flow_index % len(FLOW)
        speed = 1 + (score / UP_SPEED_AT)

        # If someone does bad, restart the flow
        if blocks and blocks[0].pos_x <= 0 and not block.cleared:
            reset()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key in KEYS.keys():
                    key_input(KEYS[event.key])

        # Do we need to add a block
        if (not blocks) or blocks[-1].right_edge() < SCREEN_SIZE[0]:
            start = blocks[-1].right_edge() if blocks else SCREEN_SIZE[0]

            # Check if we need to delete the first element
            if delete_with_next and blocks:
                del blocks[0]
                delete_with_next = False

            # Create a block, add it to the right lists and make it ready
            # for drawing.
            text = None
            if FLOW[flow_index][0] == 'DATA':
                text = hex(randint(0,2**16))[2:].zfill(4)

            block = make_block(FLOW[flow_index][0], start, text=text)
            blocks.append(block)
            devices[FLOW[flow_index][1]].add_block(block)
            flow_index = flow_index + 1

            # Add the block to the typing game
            add_typing(block)

        # BELOW THIS, THINGS ARE RELATED TO DRAWING
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(BG, BGREC)

        # Draw scores
        draw_scores()

        # Draw tranmission boxes
        draw_lines()

        pygame.display.update()

        # Move blocks
        move_lines()

        # Tick clock
        fpsClock.tick(FPS)
