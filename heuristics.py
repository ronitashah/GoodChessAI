"""has all the functions that do the heuristics"""

from .C import *
import chess
def matheuristic(self, square):
    """returns the material and position heuristic for the given square with a piece"""
    #piece = number from -6 to 6, Piece = object.
    piece = self.grid[square]
    if (piece > 0): #if piece is white
        return mateval[piece] + poseval[piece][square]
    return -mateval[-piece] - poseval[-piece][(7 - square // 8) * 8 + square % 8]
def Pheuristic(self, square):
    """returns the heuristic score for the given square with a pawn"""
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
        heuristicscore += (collength - 1) * doubleP #how bad 2 or more pawns are in same column
    #checks if there are any isolated pawns; different values for if theres none, one, or two next to the pawn
    heuristicscore += isolatedP[isolated(pawncol, col)]
    if (collength == 1):
        if (col > 0):
            t = isolated(pawncol, col - 1)
            heuristicscore += isolatedP[t] - isolatedP[t - 1]
        if (col < 7):
            t = isolated(pawncol, col + 1)
            heuristicscore += isolatedP[t] - isolatedP[t - 1]
    #passedpawn heuristic
    if (piece == 1):
        pawncol2 = self.Bpieces[1]
        if (wpassed(pawncol2, col, square // 8) == 0):
            heuristicscore += passedP + (square // 8 * passedpawncoef)
        ly = pawncol[col][0]
        if (ly == square // 8):
            if (collength > 1):
                ly = pawncol[col][1]
            else:
                ly = 8
        for y in pawncol2[col]:
            if (y <= ly and y > square // 8 and bpassed(pawncol, col, y) == 1):
                heuristicscore += passedP + (7 - (y)) * passedpawncoef
        if (col > 0):
            for y in pawncol2[col - 1]:
                if (y <= ly and y > square // 8 and bpassed(pawncol, col - 1, y) == 1):
                    heuristicscore += passedP + (7 - (y)) * passedpawncoef
        if (col < 7):
            for y in pawncol2[col + 1]:
                if (y <= ly and y > square // 8 and bpassed(pawncol, col + 1, y) == 1):
                    heuristicscore += passedP + (7 - (y)) * passedpawncoef
    if (piece == -1):
        pawncol2 = self.Wpieces[1]
        if (bpassed(pawncol2, col, square // 8) == 0):
            heuristicscore += passedP + (7 - (square // 8)) * passedpawncoef
        hy = pawncol[col][collength - 1]
        if (hy == square // 8):
            if (collength > 1):
                hy = pawncol[col][collength - 2]
            else:
                hy = 0
        if (collength == 1):
            for y in pawncol2[col]:
                if (y >= hy and y < square // 8 and wpassed(pawncol, col, y) == 1):
                    heuristicscore += passedP + (y * passedpawncoef)
            if (col > 0):
                for y in pawncol2[col - 1]:
                    if (y >= hy and y < square // 8 and wpassed(pawncol, col - 1, y) == 1):
                        heuristicscore += passedP + (y * passedpawncoef)
            if (col < 7):
                for y in pawncol2[col + 1]:
                    if (y >= hy and y < square // 8 and wpassed(pawncol, col + 1, y) == 1):
                        heuristicscore += passedP + (y * passedpawncoef)
    return heuristicscore * piece #negative if black

def isolated(pawncol, col):
    """returns how many adjacent columns to the given pawn contain a pawn"""
    ans = 0
    if (col > 0 and len(pawncol[col - 1]) > 0):
        ans += 1
    if (col < 7 and len(pawncol[col + 1]) > 0):
        ans += 1
    return ans

def wpassed(pawncol, col, y):
    """returns how many black pawn columns are preventing the given white pawn from becoming passed"""
    ans = 0 
    if (len(pawncol[col]) > 0 and y < pawncol[col][len(pawncol[col]) - 1]):
        ans += 1
    if (col > 0 and ((len(pawncol[col - 1]) > 0 and y < pawncol[col - 1][len(pawncol[col - 1])-1]))):
        ans += 1
    if (col < 7 and ((len(pawncol[col + 1]) > 0 and y < pawncol[col + 1][len(pawncol[col + 1])-1]))):
        ans += 1
    return ans
    
def bpassed(pawncol, col, y):
    """returns how many white pawn columns are preventing the given black pawn from becoming passed"""
    ans = 0
    if (len(pawncol[col]) > 0 and y > pawncol[col][0]):
        ans += 1
    if (col > 0 and ((len(pawncol[col - 1]) > 0 and y > pawncol[col - 1][0]))):
        ans += 1
    if (col < 7 and ((len(pawncol[col + 1]) > 0 and y > pawncol[col + 1][0]))):
        ans += 1
    return ans
        