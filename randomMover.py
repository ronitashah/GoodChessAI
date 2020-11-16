import random
import chess

class Player:
    def __init__(self, board, color, time):
        seed = random.randint(0, 1000000)
        random.seed(seed)
        print("seed = " + str(seed))
        pass
    
    def move(self, board, time):
        return random.choice(list(board.legal_moves))