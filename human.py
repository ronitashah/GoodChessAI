import chess
class Player:
    def __init__(self, board, color, time, endgame):
        self.first = color == chess.WHITE
        pass
    def move(self, board, time):
        if (self.first):
            self.first = False
        else:
            move = board.pop()
            print(board.san(move))
            board.push(move)
        move = None
        while (move == None):
            try:
                move = board.parse_san(input())
            except:
                print("bad")
        return move