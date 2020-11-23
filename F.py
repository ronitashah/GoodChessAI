"""miscellanious functions"""

import chess
def invert(move):
    """returns the board inverted to the opponents perspective"""
    fromS = move.from_square
    toS = move.to_square
    return chess.Move((7 - fromS // 8) * 8 + fromS % 8, (7 - toS // 8) * 8 + toS % 8, move.promotion)
def pieceof(P):
    """returns the piece type in integer form from the piece object

    white is positive, black is negative"""
    if (P.color == chess.WHITE):
        return P.piece_type
    return -P.piece_type
def insert(l, v):
    """inserts value v into an appropriate spot in sorted list l"""
    x = 0
    while x < len(l) and v >= l[x]:
        x += 1
    l.insert(x, v)
def insert2(l, v):
    """inserts tuple v into an appropriate spot in sorted list l by the first index"""
    x = 0
    while x < len(l) and v[0] >= l[x][0]:
        x += 1
    l.insert(x, v)
def insert3(l, v, k):
    """inserts value v into the appropriate spot based on value k into the sorted list l"""
    x = 0
    while x < len(l) and k >= l[x][0]:
        x += 1
    l.insert(x, v)