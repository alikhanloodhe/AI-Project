import pygame
from .constants import RED, WHITE, BLUE,YELLOW, SQUARE_SIZE
from checkers.board import Board

class Game:
    # In python we call the variables and the functions of a class using self. keyword in the same class

    def __init__(self, win): # constructor of the class game
        self._init()
        self.win = win # any data type of win will be the data type of win in the game class the variable is declared and initialized at the same time
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col): # Checking what the select function is doing over here 
        if self.selected:   # If a peice is already selected
            result = self._move(row, col) # move it to new position
            if not result:      # if there is no valid moves 
                self.selected = None # set selected to none
                self.select(row, col) # call it again recursively
        
        piece = self.board.get_piece(row, col) # select the peice from the board with the row and columns selected by mouse
        if piece != 0 and piece.color == self.turn: # Checks if there peice exists and it is the same turn for the peice
            self.selected = piece        # set selected to peice
            self.valid_moves = self.board.get_valid_moves(piece) # show the valid moves for the given peice
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            # Here we can change the color and radius of circle of valid move
            pygame.draw.circle(self.win, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)
            

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    # Getter method for a Board        
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        Board.print_kings(board)
        Board.print_pawns(board)
        self.change_turn()
    def has_valid_moves(self, board, color):
        """
        Checks if there are any valid moves for a given color on the board.

        Args:
            board: The current board state.
            color: The color of the player to check (e.g., RED or WHITE).

        Returns:
            True if there are valid moves, False otherwise.
        """
        for piece in board.get_all_peices(color):
            valid_moves = board.get_valid_moves(piece)
            if valid_moves:  # If there is at least one valid move
                return True
        return False