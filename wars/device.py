import pygame
from pygame.locals import *
from wars.block import Block

class Device(object):
    # Static params
    height = 30

    # Object params
    blocks = []
    title  = None
    pos_y  = None

    def __init__(self, title, pos):
        self.title = title
        self.pos_y = pos
        self.blocks = []

    def move_blocks(self, amount):
        for block in self.blocks:
            block.move(amount)
            if block.right_edge() <= 0:
                self.blocks.remove(block)

    def add_block(self, block):
        block.pos_y = self.pos_y * self.height
        self.blocks.append(block)

    def reset(self):
        del self.blocks[:]

    def draw(self, surface):
        # Do all the drawing of yourself ans such
        # TODO: Implement this..

        # Draw the blocks into yourself
        for block in self.blocks:
            block.draw(surface)
