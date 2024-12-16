from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self): # give the center coordinates x,y for the peice
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    def is_king(self):
        return self.king;
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        # In drawing the circle we give surface e.g win and color e.g Grey and center e.g x,y and radius
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE) # drawing the outline of the peice
        pygame.draw.circle(win, self.color, (self.x, self.y), radius) # drawing the actual peice
        if self.king:
            # blit function is to draw a surface over another surface
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2)) # drawing crown 
 
    def move(self, row, col): # Move function will give new row and column to the peice and calculates new coordinates for it
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
    def is_king(self):
        return self.king
    
    # Python __repr__() is one of the magic methods that returns a printable representation of an object in Python that can be
    # customized or predefined, i.e. we can also create the string representation of the object according to our needs