import pygame # Python Library for developing the UI
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED,WHITE # Importing the constants from the checkers
from checkers.game import Game # Importing Game file from the checkers folder
from minimax.algorithm import minimax # Importing the minimax algorithm from the minimax folder
# from minimax.algorithm import minimax ...This to be implemented

FPS = 90 # Frames rate to be used in the game

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # calling standard funtion from pygame library to display frame // similar to Jframe
pygame.display.set_caption('Checkers')         # Setting title to the frame e.g JTitle

def get_row_col_from_mouse(pos):
    x, y = pos                  # calculates the row and column by dividing with the square size 
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
    # I have to add one more thing If AI just blocked me and i have no move left the AI had a chance to capture but it neglects !!!
def main():
    run = True
    clock = pygame.time.Clock() #  Creates a new Clock object that can be used to track an amount of time. The clock also provides several functions to help control a game's framerate
    game = Game(WIN)

    while run:
        clock.tick(FPS) # Setting the frame rate of the game
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(),2, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None: # The winner function will return None until the game is over
            print(game.winner()) 
            run = False

        
        for event in pygame.event.get(): # Loop to handle the events happening in the frame
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # capture mouse event when clicked e.g action listener in java
                pos = pygame.mouse.get_pos() # The mouse coordinates in the frame will be calculated by pygame 
                row, col = get_row_col_from_mouse(pos) # give the row and column by the coordinates
                game.select(row, col) # select that box eg that row and columns where the mouse is pointed

        game.update()
    
    pygame.quit()

main()