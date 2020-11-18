import chess
from .F import *
count = 0
def minimax(gboard, depth):
    global count
    t = negascout2(gboard, depth, 1)[0][1]
    return t
def negascout1(gboard, depth, a, b, color):
    v = 0
    if (depth == 1):
        moves = list(gboard.board.legal_moves)
        if (len(moves) == 0):
            if (gboard.board.is_check()):
                return -1000000 - depth
            else:
                return 0
        for move in moves:
            gboard.push(move)
            global count
            count += 1
            v = color * gboard.heuristic
            gboard.pop()
            if (a < v):
                a = v
                if (a >= b):
                    break
        return a
    moves = negascout2(gboard, depth // 2, color)
    if (len(moves) == 0):
        if (gboard.board.is_check()):
            return -1000000 - depth
        else:
            return 0
    if (depth == 2):
        for (_, move) in moves:
            gboard.push(move)
            v = -negascout1(gboard, 1, -b, -a, -color)
            gboard.pop()
            if (a < v):
                a = v
                if (a >= b):
                    break
        return a
    for x in range(len(moves)):
        move = moves[x][1]
        gboard.push(move)
        if (x == 0):
            v = -negascout1(gboard, depth - 1, -b, -a, -color)
        else:
            v = -negascout1(gboard, depth - 1, -a - 0.01, -a, -color)
            if (a < v and v < b):
                v = -negascout1(gboard, depth - 1, -b, -v, -color)
        gboard.pop()
        if (a < v):
            a = v
            if (a >= b):
                break
    return a
def negascout2(gboard, depth, color):
    ans = []
    if (depth == 1):
        moves = list(gboard.board.legal_moves)
        for move in moves:
            gboard.push(move)
            global count
            count += 1
            v = color * gboard.heuristic
            gboard.pop()
            insert2(ans, (-v, move))
        return ans
    moves = negascout2(gboard, depth // 2, color)
    a = -float("inf")
    b = float("inf")
    v = 0
    for x in range(len(moves)):
        move = moves[x][1]
        gboard.push(move)
        if (x == 0):
            v = -negascout1(gboard, depth - 1, -b, -a, -color)
        else:
            v = -negascout1(gboard, depth - 1, -a - 0.01, -a, -color)
            if (a < v):
                v = -negascout1(gboard, depth - 1, -b, -v, -color)
        gboard.pop()
        insert2(ans, (-v, move))
        if (a < v):
            a = v
    return ans
def min(gboard, depth, a, b): #does the min part of minimax, and return the eval
    depth -= 1
    board = gboard.board
    moves = list(board.legal_moves)
    t = 0
    if (len(moves) == 0):
        if (board.is_check()):
            return 1000000 + depth
        else:
            return 0
    min = float("inf")
    for move in moves:
        gboard.push(move)
        if (depth == 0):
            global count
            count += 1
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
            return (-1000000 - depth, None)
        else:
            return (0, None)
    max = -float("inf")
    maxa = None
    t = 0
    for move in moves:
        gboard.push(move)
        if (depth == 0):
            global count
            count += 1
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