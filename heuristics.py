import C
import chess
def matheuristic(self, square):
    #piece = number from -6 to 6, Piece = object.
    piece = self.grid[square]
    if (piece > 0): #if piece is white
        return C.mateval[piece] + C.poseval[piece][square]
    return -C.mateval[-piece] - C.poseval[-piece][(7 - square // 8) * 8 + square % 8]

def isolated(pawncol, col):
    ans = 0
    if (col > 0 and len(pawncol[col - 1]) > 0):
        ans += 1
    if (col < 7 and len(pawncol[col + 1]) > 0):
        ans += 1
    return ans

def passed(pawncol, col, y, color):
    ans = 0
    if (color == 1):
        if (len(pawncol[col]) > 0 and y < pawncol[col][len(pawncol[col]) - 1]):
            ans += 1
        if (col > 0 and ((len(pawncol[col - 1]) > 0 and y < pawncol[col - 1][len(pawncol[col])-1]))):
            ans += 1
        if (col < 7 and ((len(pawncol[col + 1]) > 0 and y < pawncol[col + 1][len(pawncol[col])-1]))):
            ans += 1
        return ans
    if (len(pawncol[col]) > 0 and y > pawncol[col][0]):
        ans += 1
    if (col > 0 and ((len(pawncol[col - 1]) > 0 and y > pawncol[col - 1][0]))):
        ans += 1
    if (col < 7 and ((len(pawncol[col + 1]) > 0 and y > pawncol[col + 1][0]))):
        ans += 1
    return ans

def wpassed(pawncol, col, y):
    ans = 0
    if (len(pawncol[col]) > 0 and y < pawncol[col][len(pawncol[col]) - 1]):
        ans += 1
    if (col > 0 and ((len(pawncol[col - 1]) > 0 and y < pawncol[col - 1][len(pawncol[col - 1])-1]))):
        ans += 1
    if (col < 7 and ((len(pawncol[col + 1]) > 0 and y < pawncol[col + 1][len(pawncol[col + 1])-1]))):
        ans += 1
    return ans
    
def bpassed(pawncol, col, y):
    ans = 0
    if (len(pawncol[col]) > 0 and y > pawncol[col][0]):
        ans += 1
    if (col > 0 and ((len(pawncol[col - 1]) > 0 and y > pawncol[col - 1][0]))):
        ans += 1
    if (col < 7 and ((len(pawncol[col + 1]) > 0 and y > pawncol[col + 1][0]))):
        ans += 1
    return ans
        
def Pheuristic(self, square):
    heuristicscore = 0
    piece = self.grid[square]
    pawncol = None
    col = square % 8
    if (piece > 0):
        pawncol = self.Wpieces[1]
    else:
        pawncol = self.Bpieces[1]
    collength = len(pawncol[col])
    #double and greater pawn heuristic
    if (collength > 1):
        heuristicscore += (collength - 1) * C.doubleP #how bad 2 or more pawns are in same column
    #checks if there are any isolated pawns; different values for if theres none, one, or two next to the pawn
    heuristicscore += C.isolatedP[isolated(pawncol, col)]
    if (collength == 1):
        if (col > 0):
            t = isolated(pawncol, col - 1)
            heuristicscore += C.isolatedP[t] - C.isolatedP[t - 1]
        if (col < 7):
            t = isolated(pawncol, col + 1)
            heuristicscore += C.isolatedP[t] - C.isolatedP[t - 1]
    if (piece == 1):
        pawncol2 = self.Bpieces[1]
        if (wpassed(pawncol2, col, square // 8) == 0):
            heuristicscore += C.passedP
        if (collength == 1):
            for y in pawncol2[col]:
                if (y > square // 8 and bpassed(pawncol, col, y) == 1):
                    heuristicscore += C.passedP
            if (col > 0):
                for y in pawncol2[col - 1]:
                    if (y > square // 8 and bpassed(pawncol, col - 1, y) == 1):
                        heuristicscore += C.passedP
            if (col < 7):
                for y in pawncol2[col + 1]:
                    if (y > square // 8 and bpassed(pawncol, col + 1, y) == 1):
                        heuristicscore += C.passedP
    if (piece == -1):
        pawncol2 = self.Wpieces[1]
        if (bpassed(pawncol2, col, square // 8) == 0):
            heuristicscore += C.passedP
        if (collength == 1):
            for y in pawncol2[col]:
                if (y < square // 8 and wpassed(pawncol, col, y) == 1):
                    heuristicscore += C.passedP
            if (col > 0):
                for y in pawncol2[col - 1]:
                    if (y < square // 8 and wpassed(pawncol, col - 1, y) == 1):
                        heuristicscore += C.passedP
            if (col < 7):
                for y in pawncol2[col + 1]:
                    if (y < square // 8 and wpassed(pawncol, col + 1, y) == 1):
                        heuristicscore += C.passedP
        
    return heuristicscore * piece #negative if black