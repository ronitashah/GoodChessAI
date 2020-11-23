"""player class"""

from .minimax import minimax
from .GBoard import GBoard
from .F import *
import chess
import chess.polyglot
class Player:
    def __init__(self, board, side, time):
        self.gboard = GBoard(side)
        self.side = side
        self.prevpos = set()
        self.reader = chess.polyglot.open_reader("GoodChessAI/opening.bin")
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
        for entry in self.reader.find_all(board):
            if (max < entry.weight):
                max = entry.weight
                move = entry.move
        if (move == None):
            if (time > 10): #basic time management 
                move = minimax(self.gboard, 4, self.prevpos)
            elif (time > 4):
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