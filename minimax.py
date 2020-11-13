import chess
from heuristic import heuristic
from heuristic import overeval

def minimax(gboard, depth):
    t = max(gboard, depth, -float("inf"), float("inf"))[1]
    return t
def min(gboard, depth, a, b): #does the min part of minimax, and return the eval
    depth -= 1
    board = gboard.board
    moves = list(board.legal_moves)
    if (len(moves) == 0):
        if (board.is_check()):
            return 1000000
        else:
            return 0
    min = float("inf")
    for move in moves:
        gboard.push(move)
        if (depth == 0):
            t = gboard.heuristic
        else:
            t = max(gboard, depth, a, b)[0]
        gboard.pop()
        if (min > t):
            min = t
            if (b > min):
                b = min
                if (b <= a):
                    break
    
    return min
def max(gboard, depth, a, b): #does the max part of minimax, and returns a (eval, action) tuple
    depth -= 1
    board = gboard.board
    moves = list(board.legal_moves)
    if (len(moves) == 0):
        if (board.is_check()):
            return (-1000000, None)
        else:
            return (0, None)
    max = -float("inf")
    maxa = None
    for move in moves:
        gboard.push(move)
        if (depth == 0):
            t = gboard.heuristic
        else:
            t = min(gboard, depth, a, b)
        gboard.pop()
        if (max < t):
            max = t
            maxa = move
            if (a < max):
                a = max
                if (a >= b):
                    break
    return (max, maxa)