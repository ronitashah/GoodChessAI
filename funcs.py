import chess
def invert(move): #inverts to move between white and black's percpective
    fromS = move.from_square
    toS = move.to_square
    return chess.Move((7 - fromS // 8) * 8 + fromS % 8, (7 - toS // 8) * 8 + toS % 8, move.promotion)
def piece(P): #returns the piece number value of the piece object 
    if (P.color == chess.WHITE):
        return P.piece_type
    return -P.piece_type
def insert(l, v): #inserts v into the appropriate spot of the sorted list
    x = 0
    while x < len(l) and v > l[x]:
        x += 1
    l.insert(x, v)