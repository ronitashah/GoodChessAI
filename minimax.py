import chess
from huerestic import huerestic
from huerestic import overeval
def minimax(board, depth):
    return max(board, depth)[1]
def min(board, depth): #does the min part of minimax, and return the eval
    if (board.is_game_over()):
        return overeval(board, not board.turn)
    moves = list(board.legal_moves)
    min = float("inf")
    for move in moves:
        t = max(board.copy().push(move), depth - 1)[0]
        if (min > t):
            min = t
    return min
def max(board, depth): #does the max part of minimax, and returns a (eval, action) tuple
    if (depth == 0):
        return huerestic(board, board.turn)
    if (board.is_game_over()):
        return overeval(board, board.turn)
    moves = list(board.legal_moves)
    max = -float("inf")
    maxa = None
    for move in moves:
        t = min(board.copy().push(move), depth)
        if (max < t):
            max = t
            maxa = move
    return (max, maxa)