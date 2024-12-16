# A shallow copy imports the refernce of an object 
# A deep copy imports the actual object And if we made any changes it will not effect the actual object
from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255,255,255)

def minimax(position,depth,Max_Player,game): # position: state of the board, depth: The depth of tree we want to explre, Max_player: turn of which player, game: game object
    if depth == 0 or position.winner() !=None: # The funciton would operate on recursive calls
        return position.evaluate(), position
    if Max_Player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position,WHITE,game):
            evaluation = minimax(move,depth-1,False,game)[0]
            maxEval = max(maxEval,evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position,RED,game):
            evaluation = minimax(move,depth-1,True,game)[0]
            minEval = min(minEval,evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def get_all_moves(board,color,game):
    moves = []
    for piece in board.get_all_peices(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # To make a move we need to create a copy of the board
            # and then move the piece, if we made a move to the actual board it will effect the actual board
            # So we need to create a copy of the board
            # draw_moves(game,board,piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row,piece.col)
            new_board = simulate_move(temp_piece,move,skip,temp_board, game)
            moves.append(new_board)
    return moves

def simulate_move(piece,move,skip,board,game):
    board.move(piece,move[0],move[1])
    if skip:
        board.remove(skip)
    return board


def draw_moves(game,board,peice):
    valid_moves = board.get_valid_moves(peice)
    board.draw(game.win)
    pygame.draw.circle(game.win,(0,255,0),(peice.x,peice.y),50,5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)

def alpha_beta(position, depth, alpha, beta, max_player, game):
    """
    Implements the minimax algorithm with alpha-beta pruning.

    Args:
        position: The current board state.
        depth: The depth to explore in the game tree.
        alpha: The best already explored option along the path to the root for the maximizer.
        beta: The best already explored option along the path to the root for the minimizer.
        max_player: Boolean, True if maximizing player (White), False otherwise.
        game: The game object for board interactions.

    Returns:
        A tuple containing the evaluation value and the best board state.
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = alpha_beta(move, depth - 1, alpha, beta, False, game)[0] # As the function returns two args and we are interested in one only the evaluation value
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = alpha_beta(move, depth - 1, alpha, beta, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move
