import chess
def invert(move):
    return chess.Move(63 - move.from_square, 63 - move.to_square, move.promotion)
def piece(P):
    if (P.color == chess.WHITE):
        return P.piece_type
    return -P.piece_type
def insert(l, v):
    x = len(l) - 1
    l.append(None)
    while x > 0 and v < l[x]:
        l[x + 1] = l[x]
        x -= 1
    l[x + 1] = v