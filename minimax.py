"""minimax and quiescent search"""

import chess
from .F import *
from .C import *
count = 0
def minimax(gboard, depth, prevpos):
    """returns the best move at the current board state based on the current depth"""
    global count
    count = 0
    moves = negascout2(gboard, depth - 1, 1)
    moves = moves[:min(len(moves), prune1[depth - 1])]
    v = None
    a = -float("inf")
    b = float("inf")
    ans = None
    for (_, move) in moves:
        gboard.push(move)
        if (gboard.board.fen() in prevpos):
            v = -20
        elif (v == None):
            v = -negascout1(gboard, depth - 1, -b, -a, -1)
        else:
            v = -negascout1(gboard, depth - 1, -a - 0.01, -a, -1)
            if (a < v):
                v = -negascout1(gboard, depth - 1, -b, -v, -1)
        gboard.pop()
        if (a < v):
            a = v
            ans = move
    return ans
def quiescent(gboard, a, b, color):
    """returns the heuristic value of a node
    
    runs on states where our depth does not go deep enough to fully play out a trade"""
    global count
    count += 1
    #return color * gboard.heuristic
    flags = None
    attack = None
    if (color == 1):
        flags = gboard.Bflags.copy()
        attack = gboard.Wattack
    else:
        flags = gboard.Wflags.copy()
        attack = gboard.Battack
    score = color * gboard.heuristic
    if (a < score):
        a = score
        if (a >= b):
            return score
    for square in flags:
        (p, s) = attack[square][0]
        move = chess.Move(s, square)
        if (((color == 1 and square // 8 == 7) or (color == -1 and square // 8 == 0)) and p == 1):
            move.promotion = 5
        if (not gboard.board.is_legal(move)):
            continue
        gboard.push(move)
        v = -quiescent(gboard, -b, -a, -color)
        gboard.pop()
        if (score < v):
            score = v
            if (a < score):
                a = score
                if (a >= b):
                    break
    return score
def negascout1(gboard, depth, a, b, color):
    """returns the value of the node based on the depth of the alpha-beta pruning"""
    score = -float("inf")
    if (depth == 1):
        moves = gboard.moves()
        if (len(moves) == 0):
            if (gboard.board.is_check()):
                return -1000000 - depth
            else:
                return 0
        for move in moves:
            gboard.push(move)
            v = -quiescent(gboard, -b, -a, -color)
            gboard.pop()
            if (score < v):
                score = v
                if (a < score):
                    a = score
                    if (a >= b):
                        break
        return score
    moves = negascout2(gboard, depth - 1, color)
    if (color == 1):
        moves = moves[:min(len(moves), prune1[depth - 1])]
    else:
        moves = moves[:min(len(moves), prune2[depth - 1])]
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
            if (score < v):
                score = v
                if (a < score):
                    a = score
                    if (a >= b):
                        break
        return score
    v = None
    for (_, move) in moves:
        gboard.push(move)
        if (v == None):
            v = -negascout1(gboard, depth - 1, -b, -a, -color)
        else:
            v = -negascout1(gboard, depth - 1, -a - 0.01, -a, -color)
            if (a < v and v < b):
                v = -negascout1(gboard, depth - 1, -b, -v, -color)
        gboard.pop()
        if (score < v):
            score = v
            if (a < score):
                a = score
                if (a >= b):
                    break
    return score
def negascout2(gboard, depth, color):
    """returns the possible moves from the node (gboard) given in sorted order based on the given depth"""
    ans = []
    a = -float("inf")
    b = float("inf")
    if (depth == 1):
        moves = list(gboard.board.legal_moves)
        for move in moves:
            gboard.push(move)
            v = -quiescent(gboard, -b, -a, -color)
            gboard.pop()
            if (a < v):
                a = v
            insert2(ans, (-v, move))
        return ans
    moves = negascout2(gboard, depth - 1, color)
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