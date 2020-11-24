"""player class"""

from .minimax import minimax
from .GBoard import GBoard
from .F import *
import chess
import chess.polyglot
import chess.syzygy
class Player:
    def __init__(self, board, side, time, endgame):
        self.gboard = GBoard(side)
        self.side = side
        self.prevpos = set()
        self.opening = chess.polyglot.open_reader("nishant_ronit_ryan/opening.bin")
        self.endgame = chess.syzygy.open_tablebase(endgame)
        if (side == chess.WHITE):
            self.first = True
        else:
            self.first = False
    def move(self, board, time):
        """returns moves for the AI until the game is over"""
        if (self.first):
            self.first = False
        else:
            if (self.side == chess.WHITE):
                self.gboard.push(board.peek())
            else:
                self.gboard.push(invert(board.peek()))
        move = None
        max = -float("inf")
        if (self.gboard.piececount <= 5): #endgame table
            for m in list(board.legal_moves):
                board.push(m)
                t = -self.endgame.probe_dtz(board)
                board.pop()
                if (t != 0):
                    t = 1 / t
                if (max < t):
                    max = t
                    move = m
        else:
            for entry in self.opening.find_all(board): #opening book
                if (max < entry.weight):
                    max = entry.weight
                    move = entry.move
        if (move == None):
            if (time > 5): #basic time management 
                move = minimax(self.gboard, 4, self.prevpos)
            elif (time > 1):
                move = minimax(self.gboard, 3, self.prevpos)
            else:
                move = minimax(self.gboard, 2, self.prevpos)
        elif (self.side == chess.BLACK):
            move = invert(move)
        self.gboard.push(move)
        self.prevpos.add(self.gboard.board.fen())
        if (self.side == chess.WHITE):
            return move
        return invert(move)