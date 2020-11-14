import chess
import funcs 
import C
class GBoard:
    from heuristics import matheuristic, Pheuristic
    def __init__(self, side):
        self.grid = [0 for s in range(64)]
        self.Wpieces = [[] for x in range(7)]
        self.Bpieces = [[] for x in range(7)]
        self.Wpieces[1] = [[] for x in range(8)]
        self.Bpieces[1] = [[] for x in range(8)]
        """self.Wattack = [[] for s in range(64)]
        self.Battack = [[] for s in range(64)]"""
        self.heuristic = 0
        self.movestack = []
        self.board = chess.Board()
        for s in range(64):
            self.board.remove_piece_at(s)
        t = chess.Board()
        for s in range(64):
            P = t.piece_at(s)
            if (P != None):
                self.board.set_piece_at(s, P)
                self.addpiece(s, funcs.piece(P))
        self.board.turn = side 
    def addpiece(self, square, piece): #function to be called when changing a square from empty to having a piece. updates all of the fields and heurisitc to have the piece added, but the board has the piece already added
        grid = self.grid
        grid[square] = piece
        """attack1 = None
        attack2 = None
        ptype = 0"""
        if (piece > 0):
            """attack1 = self.Wattack
            attack2 = self.Battack
            ptype = piece"""
            if (piece > 1):
                self.Wpieces[piece].append(square)
            else:
                WPC = self.Wpieces[1]
                funcs.insert(WPC[square % 8], square // 8)
        else:
            """attack1 = self.Battack
            attack2 = self.Wattack
            ptype = -piece"""
            if (piece < -1):
                self.Bpieces[-piece].append(square)
            else:
                BPC = self.Bpieces[1]
                funcs.insert(BPC[square % 8], square // 8)
        """board = self.board
        for s in board.attacks(square):
            funcs.insert(attack1[s], ptype)
        for p in attack2[square]:
            if (p == 3 or )"""
        pval = self.matheuristic(square)
        if (piece == 1 or piece == -1):
            pval += self.Pheuristic(square)
        self.heuristic += pval
    def rmpiece(self, square, piece): #function to be called when changing a square from housing the piece "piece" into empty. updates all of the field and heuristicto have the piece removed, but the board already has the piece removed
        pval = self.matheuristic(square)
        if (piece == 1 or piece == -1):
            pval += self.Pheuristic(square)
        grid = self.grid
        grid[square] = 0
        if (piece > 0):
            if (piece > 1):
                self.Wpieces[piece].remove(square)
            else:
                WPC = self.Wpieces[1]
                WPC[square % 8].remove(square // 8)
        else:
            if (piece < -1):
                self.Bpieces[-piece].remove(square)
            else:
                BPC = self.Bpieces[1]
                BPC[square % 8].remove(square // 8)
        self.heuristic -= pval
    def push(self, move): #makes the move and calls addpiece and rmpiece appriopriately to make the changes to all of the fields(other than obard which is updated seperately)
        grid = self.grid
        board = self.board
        board.turn = not board.turn
        fromS = move.from_square
        toS = move.to_square
        piece = grid[fromS]
        P1 = board.remove_piece_at(fromS)
        self.rmpiece(fromS, piece)
        if ((piece == 6 or piece == -6) and (toS - fromS == 2 or toS - fromS == -2)):
            RSI = 0
            RSF = 0
            if (toS > fromS):
                RSI = toS + 1
                RSF = toS - 1
            else:
                RSI = toS - 2
                RSF = toS + 1
            Rpiece = grid[RSI]
            P2 = board.remove_piece_at(RSI)
            self.rmpiece(RSI, Rpiece)
            board.set_piece_at(toS, P1)
            self.addpiece(toS, piece)
            board.set_piece_at(RSF, P2)
            self.addpiece(RSF, Rpiece)
            self.movestack.append((move, None, False))
        elif (grid[toS] != 0):
            P2 = board.remove_piece_at(toS)
            self.rmpiece(toS, grid[toS])
            if (move.promotion != None):
                P3 = chess.Piece(move.promotion, P1.color)
                board.set_piece_at(toS, P3)
                self.addpiece(toS, funcs.piece(P3))
            else:
                board.set_piece_at(toS, P1)
                self.addpiece(toS, piece)
            self.movestack.append((move, P2, False))
        elif ((piece == 1 or piece == -1) and (toS - fromS) % 8 != 0):
            capS = 0
            if (piece == 1):
                capS = toS - 8
            else:
                capS = toS + 8
            P2 = board.remove_piece_at(capS)
            self.rmpiece(capS, grid[capS])
            board.set_piece_at(toS, P1)
            self.addpiece(toS, piece)
            self.movestack.append((move, P2, True))
        else:
            if (move.promotion != None):
                P3 = chess.Piece(move.promotion, P1.color)
                board.set_piece_at(toS, P3)
                self.addpiece(toS, funcs.piece(P3))
            else:
                board.set_piece_at(toS, P1)
                self.addpiece(toS, piece)
            self.movestack.append((move, None, False))
    def pop(self): #undoes the prev move and calls addpiece and rmpiece appriopriately to make the changes to all of the fields(other than obard which is updated seperately)
        grid = self.grid
        board = self.board
        board.turn = not board.turn
        (move, P2, en) = self.movestack.pop()
        fromS = move.from_square
        toS = move.to_square
        piece = grid[toS]
        P1 = board.remove_piece_at(toS)
        self.rmpiece(toS, piece)
        if ((piece == 6 or piece == -6) and (toS - fromS == 2 or toS - fromS == -2)):
            RSI = 0
            RSF = 0
            if (toS > fromS):
                RSI = toS + 1
                RSF = toS - 1
            else:
                RSI = toS - 2
                RSF = toS + 1
            Rpiece = grid[RSF]
            P2 = board.remove_piece_at(RSF)
            self.rmpiece(RSF, Rpiece)
            board.set_piece_at(fromS, P1)
            self.addpiece(fromS, piece)
            board.set_piece_at(RSI, P2)
            self.addpiece(RSI, Rpiece)
        elif (en):
            capS = 0
            if (piece == 1):
                capS = toS - 8
            else:
                capS = toS + 8
            board.set_piece_at(fromS, P1)
            self.addpiece(fromS, piece)
            board.set_piece_at(capS, P2)
            self.addpiece(capS, funcs.piece(P2))
        else:
            if (move.promotion != None):
                board.set_piece_at(fromS, chess.Piece(1, P1.color))
                if (P1.color == chess.WHITE):
                    self.addpiece(fromS, 1)
                else:
                    self.addpiece(fromS, -1)
            else:
                board.set_piece_at(fromS, P1)
                self.addpiece(fromS, piece)
            if (P2 != None):
                board.set_piece_at(toS, P2)
                self.addpiece(toS, funcs.piece(P2))
        return move
    def peek(self):
        return self.movestack[-1]
    