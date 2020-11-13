import chess
from heuristic import heuristic
from heuristic import overeval

def minimax(gboard, depth):
    t = max(gboard, depth, -float("inf"), float("inf"))[1]
    return t
def min(gboard, depth, a, b): #does the min part of minimax, and return the eval
    board = gboard.board
    if (board.is_game_over()):
        return overeval(board, not board.turn)
    moves = list(board.legal_moves)
    min = None
    for move in moves:
        gboard.push(move)
        t = max(gboard, depth - 1, a, b)[0]
        gboard.pop()
        if (min == None or min > t):
            min = t
            if (b > min):
                b = min
                if (b <= a):
                    break
    return min
def max(gboard, depth, a, b): #does the max part of minimax, and returns a (eval, action) tuple
    if (depth == 0):
        return (gboard.heuristic, None)
    board = gboard.board
    if (board.is_game_over()):
        return (overeval(board, board.turn), None)
    moves = list(board.legal_moves)
    max = None
    maxa = None
    for move in moves:
        gboard.push(move)
        t = min(gboard, depth, a, b)
        gboard.pop()
        if (max == None or max < t):
            max = t
            maxa = move
            if (a < max):
                a = max
                if (a >= b):
                    break
    return (max, maxa)