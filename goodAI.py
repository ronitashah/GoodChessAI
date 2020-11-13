from minimax import minimax
from GBoard import GBoard
import funcs
import chess
import C
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
                self.gboard.push(funcs.invert(board.peek()))
        move = minimax(self.gboard, 2)
        self.gboard.push(move)
        if (self.side == chess.WHITE):
            return move
        return funcs.invert(move)