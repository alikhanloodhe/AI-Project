import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE,BLUE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = [] # declaring board as an array
        self.red_pawn = self.white_pawn = 12 # initializing the pawns to 12
        self.red_kings = self.white_kings = 0 # initializing the queen/ Kings to 0
        self.create_board()
    
    def draw_squares(self, win): # what is this win? Win is actually the surface object in the pygame library
        win.fill(BLACK) # The whole board is fill with black color and then white squares are drawn on it
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):  # white square are drawn alternatively
                pygame.draw.rect(win, BLUE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # inbuilt func to draw squar

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] # swap peice box and normal box
        piece.move(row, col) # call move func of the peice class that changes the internal coordinates of the peice

        # Here it also has some kinds of problems It starts by making the red as 1 king
        if row == ROWS - 1 or row == 0: # make the king if peice enters the territory of the other side
            if not piece.is_king():
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                    self.white_pawn -= 1
                else:
                    self.red_kings += 1 
                    self.red_pawn -= 1
                

    def get_piece(self, row, col): # as board is a two dimensional array get_peice will give the element at the given row and col 
        return self.board[row][col] 
    
    
    #Firstly we will define an evaluation funciton that will give us the value of the board at any given time
    def evaluate(self): # We can make this evaluation function as much complex as we can The more complex it is the more efficient our AI would be
        return self.white_pawn-self.red_pawn + (self.white_kings * 0.5 -self.red_kings * 0.5)
    # Get all the peices of a color
    def get_all_peices(self,color):
        peices = []
        for row in self.board:
            for peice in row:
                if peice!=0 and peice.color == color :
                    peices.append(peice)
        return peices



    # The very first step is creating a board
    def create_board(self):
        for row in range(ROWS):
            self.board.append([]) # here it will append an array of rows in the other array e.g creating a two d array
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2): # Conditions to place the peices at the specific positions
                    if row < 3: # For white ones
                        self.board[row].append(Piece(row, col, WHITE)) # Creating an object of peice and append it to the array the white ones
                    elif row > 4: # For red ones
                        self.board[row].append(Piece(row, col, RED))    # Creating an object of peice and append it to the array the red ones
                    else:
                        self.board[row].append(0) # filling the rest of the board with 0's
                else:
                    self.board[row].append(0) # filling the rest of the board with 0's
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:  # as in create board function all the places other than peices are initialized to 0 
                    piece.draw(win) # drawing peices from peice class || the peice object is at different positions of the board

    def remove(self, pieces): # to remove captured peices
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    if piece.is_king():
                        self.red_kings -= 1
                    else:
                        self.red_pawn -= 1
                else:
                    if piece.is_king():
                        self.white_kings -=1
                    else:
                        self.white_pawn -= 1
    
    def winner(self): # if any of the peices become 0 than winner function return the one which win
        if self.red_pawn <= 0 and self.red_kings<=0:
            return WHITE 
        elif self.white_pawn <= 0 and self.white_kings<=0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step): # This will check that the left move of peice is not the wall 
            if left < 0:
                break
            
            current = self.board[r][left] 
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    def print_kings(board):
        print(f"Red Kings: {board.red_kings} white kings: {board.white_kings}")
    def print_pawns(board):
        print(f"Red Pawns: {board.red_pawn} White Pawns: {board.white_pawn}")