"""our own board class"""

import chess
from .F import *
from .C import *
class GBoard:
    """our own board class that has extra fields for heuristic calculations that are incrementally updated"""
    from .heuristics import matheuristic, Pheuristic
    def __init__(self, side):
        self.grid = [0 for s in range(64)]
        self.Wpieces = [[] for x in range(7)]
        self.Bpieces = [[] for x in range(7)]
        self.Wpieces[1] = [[] for x in range(8)]
        self.Bpieces[1] = [[] for x in range(8)]
        self.piececount = 0
        self.Wattack = [[] for s in range(64)]
        self.Battack = [[] for s in range(64)]
        self.castle = 3
        self.heuristic = 0
        self.heuristicstack = [self.heuristic]
        self.movestack = []
        self.castlestack = [self.castle]
        self.Wflags = set()
        self.Bflags = set()
        self.changed = set()
        self.board = chess.Board()
        for s in range(64):
            self.board.remove_piece_at(s)
        t = chess.Board()
        for s in range(64):
            P = t.piece_at(s)
            if (P != None):
                self.board.set_piece_at(s, P)
                self.addpiece(s, pieceof(P), False)
        self.board.turn = side 
    def addpiece(self, square, piece, h):
        """updates all the fields and heuristics to have the piece added, but the board has the piece already added
        
        should be called when changing a square from empty to having a piece
        """
        self.piececount += 1
        grid = self.grid
        attack1 = None
        attack2 = None
        color = 0
        if (piece > 0):
            attack1 = self.Wattack
            attack2 = self.Battack
            color = 1
            if (piece > 1):
                self.Wpieces[piece].append(square)
            else:
                WPC = self.Wpieces[1]
                insert(WPC[square % 8], square // 8)
        else:
            attack1 = self.Battack
            attack2 = self.Wattack
            color = -1
            if (piece < -1):
                self.Bpieces[-piece].append(square)
            else:
                BPC = self.Bpieces[1]
                insert(BPC[square % 8], square // 8)
        ptype = color * piece
        #updates the attacks arrays
        changed = self.changed
        changed.add(square)
        x = square % 8
        y = square // 8
        for s in self.board.attacks(square):
            insert2(attack1[s], (ptype, square))
            changed.add(s)
            p = grid[s]
            if (p != 0):
                ap = abs(p)
                if (ptype > ap):
                    for sq in sync(grid, x, y, piece, s % 8, s // 8, s, p):
                        changed.add(sq)
                        insert2(attack1[sq], (ptype, square))
                else:
                    for sq in sync(grid, x, y, piece, s % 8, s // 8, s, p):
                        changed.add(sq)
                        attack1[sq].insert(attack1[sq].index((ap, s)) + 1, (ptype, square))
        for (ap, s) in attack1[square]:
            p = ap * color
            for sq in blocks(grid, s % 8, s // 8, p, x, y, square):
                changed.add(sq)
                attack1[sq].remove((ap, s))
            if (ap > ptype):
                for sq in sync(grid, s % 8, s // 8, p, x, y, square, piece):
                    insert2(attack1[sq], (ap, s))
            else:
                for sq in sync(grid, s % 8, s // 8, p, x, y, square, piece):
                    attack1[sq].insert(attack1[sq].index((ptype, square)) + 1, (ap, s))
        for (ap, s) in attack2[square]:
            p = -ap * color
            for sq in blocks(grid, s % 8, s // 8, p, x, y, square):
                changed.add(sq)
                attack2[sq].remove((ap, s))
        grid[square] = piece
        if (h):
            pval = self.matheuristic(square)
            if (piece == 1 or piece == -1):
                pval += self.Pheuristic(square)
            self.heuristic += pval
    def rmpiece(self, square, piece, h): 
        """function to be called when changing a square from housing the piece "piece" into empty. updates all of the field and heuristicto have the piece removed, and the board doesn't have the piece removed"""
        self.piececount -= 1
        if (h):
            pval = self.matheuristic(square)
            if (piece == 1 or piece == -1):
                pval += self.Pheuristic(square)
            self.heuristic -= pval
        grid = self.grid
        grid[square] = 0
        attack1 = None
        attack2 = None
        color = 0
        if (piece > 0):
            attack1 = self.Wattack
            attack2 = self.Battack
            color = 1
            if (piece > 1):
                self.Wpieces[piece].remove(square)
            else:
                WPC = self.Wpieces[1]
                WPC[square % 8].remove(square // 8)
        else:
            attack1 = self.Battack
            attack2 = self.Wattack
            color = -1
            if (piece < -1):
                self.Bpieces[-piece].remove(square)
            else:
                BPC = self.Bpieces[1]
                BPC[square % 8].remove(square // 8)
        ptype = color * piece
        #updates the attacks arrays
        changed = self.changed
        changed.add(square)
        x = square % 8
        y = square // 8
        for s in self.board.attacks(square):
            attack1[s].remove((ptype, square))
            changed.add(s)
            p = grid[s]
            if (p != 0):
                for sq in sync(grid, x, y, piece, s % 8, s // 8, s, p):
                    changed.add(sq)
                    attack1[sq].remove((ptype, square))
        max = 0
        for (ap, s) in attack1[square]:
            p = color * ap
            for sq in sync(grid, s % 8, s // 8, p, x, y, square, piece):
                attack1[sq].remove((ap, s))
            if (max < ap):
                max = ap
            tmax = max
            for sq in blocks(grid, s % 8, s // 8, p, x, y, square):
                changed.add(sq)
                insert3(attack1[sq], (ap, s), tmax)
                pi = abs(grid[sq])
                if (tmax < pi):
                    tmax = pi
        max = 0
        for (ap, s) in attack2[square]:
            p = -color * ap
            if (max < ap):
                max = ap
            tmax = max
            for sq in blocks(grid, s % 8, s // 8, p, x, y, square):
                changed.add(sq)
                insert3(attack2[sq], (ap, s), tmax)
                pi = abs(grid[sq])
                if (tmax < pi):
                    tmax = pi
    def moves(self):
        board = self.board
        castle = self.castle
        ans = list(board.legal_moves)
        x = 0
        while (x < len(ans)):
            if (board.is_castling(ans[x])):
                if (board.turn):
                    if ((castle & 1) == 0):
                        del ans[x]
                    return ans
                if ((castle & 2) == 0):
                    del ans[x]
                return ans
            x += 1
        return ans
    def push(self, move): 
        """makes the move and calls addpiece and rmpiece appriopriately to make the changes to all of the fields(other than obard which is updated seperately)"""
        grid = self.grid
        board = self.board
        board.turn = not board.turn
        fromS = move.from_square
        toS = move.to_square
        piece = grid[fromS]
        self.rmpiece(fromS, piece, True)
        P1 = board.remove_piece_at(fromS)
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
            self.rmpiece(RSI, Rpiece, True)
            P2 = board.remove_piece_at(RSI)
            board.set_piece_at(toS, P1)
            self.addpiece(toS, piece, True)
            board.set_piece_at(RSF, P2)
            self.addpiece(RSF, Rpiece, True)
            self.movestack.append((move, None, False))
        elif (grid[toS] != 0):
            self.rmpiece(toS, grid[toS], True)
            P2 = board.remove_piece_at(toS)
            if (move.promotion != None):
                P3 = chess.Piece(move.promotion, P1.color)
                board.set_piece_at(toS, P3)
                self.addpiece(toS, pieceof(P3), True)
            else:
                board.set_piece_at(toS, P1)
                self.addpiece(toS, piece, True)
            self.movestack.append((move, P2, False))
        elif ((piece == 1 or piece == -1) and (toS - fromS) % 8 != 0):
            capS = 0
            if (piece == 1):
                capS = toS - 8
            else:
                capS = toS + 8
            self.rmpiece(capS, grid[capS], True)
            P2 = board.remove_piece_at(capS)
            board.set_piece_at(toS, P1)
            self.addpiece(toS, piece, True)
            self.movestack.append((move, P2, True))
        else:
            if (move.promotion != None):
                P3 = chess.Piece(move.promotion, P1.color)
                board.set_piece_at(toS, P3)
                self.addpiece(toS, pieceof(P3), True)
            else:
                board.set_piece_at(toS, P1)
                self.addpiece(toS, piece, True)
            self.movestack.append((move, None, False))
        Wflags1 = self.Wflags
        Bflags1 = self.Bflags
        Wflags2 = set()
        Bflags2 = set()
        Wattack = self.Wattack
        Battack = self.Battack
        for square in Wflags1:
            p = grid[square]
            if (p > 0 and flag(Wattack[square], Battack[square], p)):
                Wflags2.add(square)
        for square in Bflags1:
            p = grid[square]
            if (p < 0 and flag(Battack[square], Wattack[square], -p)):
                Bflags2.add(square)
        for square in self.changed:
            Wa = Wattack[square]
            Ba = Battack[square]
            p = grid[square]
            if (p > 0 and flag(Wa, Ba, p)):
                Wflags2.add(square)
            elif (p < 0 and flag(Ba, Wa, -p)):
                Bflags2.add(square)
        self.Wflags = Wflags2
        self.Bflags = Bflags2
        self.changed = set()
        castle = self.castle
        if (piece == 6 and castle & 1 == 1):
            castle -= 1
            self.heuristic -= castleval
        elif (piece == -6 and castle & 2 == 1):
            castle -= 2
            self.heuristic += castleval
        self.castlestack.append(castle)
        self.heuristicstack.append(self.heuristic)
    def pop(self): 
        """undoes the prev move and calls addpiece and rmpiece appriopriately to make the changes to all of the fields(other than obard which is updated seperately)"""
        grid = self.grid
        board = self.board
        board.turn = not board.turn
        (move, P2, en) = self.movestack.pop()
        fromS = move.from_square
        toS = move.to_square
        piece = grid[toS]
        self.rmpiece(toS, piece, False)
        P1 = board.remove_piece_at(toS)
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
            self.rmpiece(RSF, Rpiece, False)
            P2 = board.remove_piece_at(RSF)
            board.set_piece_at(fromS, P1)
            self.addpiece(fromS, piece, False)
            board.set_piece_at(RSI, P2)
            self.addpiece(RSI, Rpiece, False)
        elif (en):
            capS = 0
            if (piece == 1):
                capS = toS - 8
            else:
                capS = toS + 8
            board.set_piece_at(fromS, P1)
            self.addpiece(fromS, piece, False)
            board.set_piece_at(capS, P2)
            self.addpiece(capS, pieceof(P2), False)
        else:
            if (move.promotion != None):
                board.set_piece_at(fromS, chess.Piece(1, P1.color))
                if (P1.color == chess.WHITE):
                    self.addpiece(fromS, 1, False)
                else:
                    self.addpiece(fromS, -1, False)
            else:
                board.set_piece_at(fromS, P1)
                self.addpiece(fromS, piece, False)
            if (P2 != None):
                board.set_piece_at(toS, P2)
                self.addpiece(toS, pieceof(P2), False)
        castlestack = self.castlestack
        castlestack.pop()
        self.castle = castlestack[len(castlestack) - 1]
        hstack = self.heuristicstack
        hstack.pop()
        self.heuristic = hstack[len(hstack) - 1]
        return move
    def peek(self):
        """isn't used, but is there because there's also a push and pop"""
        return self.movestack[-1]
def flag(defense, attack, ptype): 
    """returns if the piece is hanging or not"""
    if(len(attack) == 0):
        return False
    i = 0
    totalyou = 0
    totalopponent = mateval[ptype]
    while (i < len(defense)):
        totalyou += mateval[attack[i][0]]
        if (totalopponent > totalyou):
            return True
        i += 1
        if (i < len(attack)):
            totalopponent += mateval[defense[i-1][0]]
        else:
            break
    if (totalopponent > totalyou):
        return True
    return False
    
def blocks(grid, fromX, fromY, fromP, toX, toY, toS):
    """returns a list of squares that the from piece is clocked by the to piece"""
    if (fromP > 5 or fromP < -5 or (fromP < 3 and fromP > -3)):
        return []
    ans = []
    if (toX == fromX):
        if (toY > fromY):
            while(toY < 7):
                toY += 1
                toS += 8
                ans.append(toS)
                p = grid[toS]
                if (p != 0):
                    return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
            return ans
        while(toY > 0):
            toY -= 1
            toS -= 8
            ans.append(toS)
            p = grid[toS]
            if (p != 0):
                return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
        return ans
    if (toY == fromY):
        if (toX > fromX):
            while(toX < 7):
                toX += 1
                toS += 1
                ans.append(toS)
                p = grid[toS]
                if (p != 0):
                    return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
            return ans
        while(toX > 0):
            toX -= 1
            toS -= 1
            ans.append(toS)
            p = grid[toS]
            if (p != 0):
                return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
        return ans
    if (toY > fromY):
        if (toX > fromX):
            if (abs(grid[toS - 9]) == 1):
                return []
            while(toX < 7 and toY < 7):
                toX += 1
                toY += 1
                toS += 9
                ans.append(toS)
                p = grid[toS]
                if (p != 0):
                    return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
            return ans
        if (abs(grid[toS - 7]) == 1):
            return []
        while(toX > 0 and toY < 7):
            toX -= 1
            toY += 1
            toS += 7
            ans.append(toS)
            p = grid[toS]
            if (p != 0):
                return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
        return ans
    if (toX > fromX):
        if (abs(grid[toS + 7]) == 1):
            return []
        while(toX < 7 and toY > 0):
            toX += 1
            toY -= 1
            toS -= 7
            ans.append(toS)
            p = grid[toS]
            if (p != 0):
                return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
        return ans
    if (abs(grid[toS + 9]) == 1):
        return []
    while(toX > 0 and toY > 0):
        toX -= 1
        toY -= 1
        toS -= 9
        ans.append(toS)
        p = grid[toS]
        if (p != 0):
            return ans + sync(grid, fromX, fromY, fromP, toX, toY, toS, p)
    return ans
def sync(grid, fromX, fromY, fromP, toX, toY, toS, toP):
    """returns a list of squares that the from piece can attack through the to piece"""
    if ((fromP > 0 and (toP < 0 or fromP < 3 or fromP > 5 or (toP != 1 and (toP < 3 or toP > 5)))) or (fromP < 0 and (toP > 0 or fromP > -3 or fromP < -5 or (toP != -1 and (toP > -3 or toP < -5))))):
        return []
    if (fromX == toX or fromY == toY):
        if (toP != 4 and toP != 5 and toP != -4 and toP != -5):
            return []
        return blocks(grid, fromX, fromY, fromP, toX, toY, toS)
    if (toP == 1 or toP == -1):
        if (toP == 1):
            if (toY < fromY):
                return []
            if (toX > fromX):
                if (toX == 7 or grid[toS - 9] == 1):
                    return []
                return [toS + 9]
            if (toX == 0 or grid[toS - 7] == 1):
                return []
            return [toS + 7]
        if (toY > fromY):
            return []
        if (toX > fromX):
            if (toX == 7 or grid[toS + 7] == -1):
                return []
            return [toS - 7]
        if (toX == 0 or grid[toS + 9] == -1):
            return []
        return [toS - 9]
    if (toP == 4 or toP == -4):
        return []
    return blocks(grid, fromX, fromY, fromP, toX, toY, toS)