import chess
from heurestic import heurestic
from heurestic import overeval
def minimax(board, depth):
    return max(board, depth)[1]
def min(board, depth): #does the min part of minimax, and return the eval
    if (board.is_game_over()):
        return overeval(board, not board.turn)
    moves = list(board.legal_moves)
    min = float("inf")
    for move in moves:
        b = board.copy()
        b.push(move)
        t = max(b, depth - 1)[0]
        if (min > t):
            min = t
    return min
def max(board, depth): #does the max part of minimax, and returns a (eval, action) tuple
    if (depth == 0):
        return (heurestic(board, board.turn), None)
    if (board.is_game_over()):
        return (overeval(board, board.turn), None)
    moves = list(board.legal_moves)
    max = -float("inf")
    maxa = None
    for move in moves:
        b = board.copy()
        b.push(move)
        t = min(b, depth)
        if (max < t):
            max = t
            maxa = move
    return (max, maxa)