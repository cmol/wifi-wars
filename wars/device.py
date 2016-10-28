import pygame
from pygame.locals import *
from block import Block

class Device(object):

    # Object params
    blocks = []

    def __init__(self):
        pass

    def move_blocks(self, amount):
        for block in blocks:
            block.move(amount)


