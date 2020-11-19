import chess
from .F import *
from .C import *
count = 0
def minimax(gboard, depth, prevpos):
    global count
    count = 0
    prune1[depth] = float("inf")
    moves = negascout2(gboard, depth, 1)
    for (v, ans) in moves:
        v *= -1
        gboard.push(ans)
        fen = gboard.board.fen()
        gboard.pop()
        if (fen in prevpos):
            continue
        if (v > -20):
            return ans
        return moves[0][1]
    return moves[0][1]
def quiescent(gboard, a, b, color):
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
    v = 0
    score = -float("inf")
    if (depth == 1):
        moves = list(gboard.board.legal_moves)
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
            if (score < v):
                score = v
                if (a < score):
                    a = score
                    if (a >= b):
                        break
        return score
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
        if (score < v):
            score = v
            if (a < score):
                a = score
                if (a >= b):
                    break
    return score
def negascout2(gboard, depth, color):
    ans = []
    a = -float("inf")
    b = float("inf")
    if (depth == 1):
        moves = list(gboard.board.legal_moves)
        for move in moves:
            gboard.push(move)
            v = -quiescent(gboard, -b, -a, -color)
            if (a < v):
                a = v
            gboard.pop()
            insert2(ans, (-v, move))
        if (color == 1):
            return ans[:min(len(ans), prune1[1])]
        else:
            return ans[:min(len(ans), prune2[1])]
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
    if (color == 1):
        return ans[:min(len(ans), prune1[depth])]
    else:
        return ans[:min(len(ans), prune2[depth])]