import chess
from heuristic import heuristic
from heuristic import overeval

count = 0
def minimax(board, depth):
    global count
    count = 0
    board.clear_stack()
    t = max(board, depth, -float("inf"), float("inf"), {})[1]
    if (t == None):
        print(board)
    #print(count)
    return t
def min(board, depth, a, b, prevboards): #does the min part of minimax, and return the eval
    if (board.is_game_over()):
        return overeval(board, not board.turn)
    #transposition table
    fen = board.fen()
    temp = prevboards.get(fen)
    if temp != None:
        return temp[0] 
    moves = list(board.legal_moves)
    min = None
    for move in moves:
        c = board.copy()
        c.push(move)
        c.clear_stack()
        t = max(c, depth - 1, a, b, prevboards)[0]
        if (min == None or min > t):
            min = t
            if (b > min):
                b = min
                if (b <= a):
                    break
    prevboards[fen] = (min, None)
    return min
def max(board, depth, a, b, prevboards): #does the max part of minimax, and returns a (eval, action) tuple
    if (depth == 0):
        global count
        count += 1
        return (heuristic(board, board.turn), None)
    if (board.is_game_over()):
        return (overeval(board, board.turn), None)
    #transposition table
    fen = board.fen()
    temp = prevboards.get(fen)
    if temp != None:
        return temp
    moves = list(board.legal_moves)
    max = None
    maxa = None
    for move in moves:
        c = board.copy()
        c.push(move)
        c.clear_stack()
        t = min(c, depth, a, b, prevboards)
        if (max == None or max < t):
            max = t
            maxa = move
            if (a < max):
                a = max
                if (a >= b):
                    break
    prevboards[fen] = (max, maxa)
    return (max, maxa)