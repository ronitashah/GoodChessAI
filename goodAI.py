from .minimax import minimax
from .GBoard import GBoard
from .F import *
import chess
class Player:
    def __init__(self, board, side, time):
        self.gboard = GBoard(side)
        self.side = side
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
        if (time > 5):
            move = minimax(self.gboard, 4)
        elif (time > 0.5):
            move = minimax(self.gboard, 3)
        else:
            move = minimax(self.gboard, 2)
        self.gboard.push(move)
        if (self.side == chess.WHITE):
            return move
        return invert(move)