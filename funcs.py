import chess
def invert(move): #inverts to move between white and black's percpective
    return chess.Move(63 - move.from_square, 63 - move.to_square, move.promotion)
def piece(P): #returns the piece number value of the piece object 
    if (P.color == chess.WHITE):
        return P.piece_type
    return -P.piece_type
def insert(l, v): #inserts v into the appropriate spot of the sorted list
    x = len(l) - 1
    l.append(None)
    while x > 0 and v < l[x]:
        l[x + 1] = l[x]
        x -= 1
    l[x + 1] = v