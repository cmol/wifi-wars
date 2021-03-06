import pygame
from pygame.locals import *

class Block(object):

    # Static params
    height = 60
    font   = pygame.font.Font(None, 42)

    # Object params
    size       = None
    pos_x      = None
    pos_y      = None
    box_text   = None
    color      = None
    text_color = None
    cleared    = False

    def __init__(self, **args):
        self.size       = args['size']
        self.pos_x      = args['start']
        self.box_text   = args['text']
        self.color      = args['color']
        self.text_color = args['text_color']

    def move(self, amount):
        self.pos_x = self.pos_x - amount

    def range(self):
        return range(self.pos_x, self.pos_x + size)

    def right_edge(self):
        return self.pos_x + self.size

    def clear(self):
        self.cleared = True
        self.color = (0,255,0)

    def draw(self, surface):
        # Draw the box
        pygame.draw.rect(surface, self.color,
                (self.pos_x, self.pos_y, self.size, self.height))

        # Draw the text in the box
        text = self.font.render(self.box_text, True, self.text_color)
        textpos = text.get_rect()
        textpos.center = (self.pos_x + self.size / 2,
                self.pos_y + self.height / 2)
        surface.blit(text, textpos)


