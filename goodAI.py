from .minimax import minimax
from .GBoard import GBoard
from .F import *
import chess
class Player:
    def __init__(self, board, side, time):
        self.gboard = GBoard(side)
        self.side = side
        self.prevpos = set()
        if (side == chess.WHITE):
            self.first = True
        else:
            self.first = False
    def move(self, board, time):
        if (self.first):
            self.first = False
        else:
            if (self.side == chess.WHITE):
                self.gboard.push(board.peek())
            else:
                self.gboard.push(invert(board.peek()))
        move = None
        if (time > 10):
            move = minimax(self.gboard, 5, self.prevpos)
        elif (time > 4):
            move = minimax(self.gboard, 4, self.prevpos)
        elif (time > 1):
            move = minimax(self.gboard, 3, self.prevpos)
        else:
            move = minimax(self.gboard, 2, self.prevpos)
        self.gboard.push(move)
        self.prevpos.add(self.gboard.board.fen())
        if (self.side == chess.WHITE):
            return move
        return invert(move)