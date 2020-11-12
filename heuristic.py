import chess
import C
def halfheuristic(board): #should run the heuristic from whites percpective and look primarly at white's things(like only white's material and stuff)
    heuristicscore = 0
    #grid setup to represent the board
    grid = [['' for i in range(8)] for j in range(8)]
    #sparse array pawn representation for both colors
    wpawncol = [[] for i in range(8)]
    bpawncol = [[] for i in range(8)]
    for x in range(8):
        for y in range(8):
            piece = board.piece_at(chess.SQUARES[x + 8 * y])
            if (piece == None):
                grid[x][y] = ' '
            else:
                grid[x][y] = piece.symbol()
                if (piece.color == chess.WHITE):
                    heuristicscore += C.mateval[grid[x][y]] + C.poseval[grid[x][y]][x + 8 * y]
            #checking if there is a pawn
            if (grid[x][y] == 'P'):
                wpawncol[x].append(y)
            if (grid[x][y] == 'p'):
                bpawncol[x].append(y)
    lastcolP = False
    for x in range(8):
        #counts the number of pawn islands
        if((not lastcolP) and len(wpawncol[x]) > 0):
            heuristicscore += C.islandP
        lastcolP = (len(wpawncol[x]) == 0)
        #checks if 2 pawns are in the same column
        if (len(wpawncol[x]) > 1):
            heuristicscore += (len(wpawncol[x]) - 1) * C.doubleP #how bad 2 pawns are in same column
        #checks if there are any isolated columns
        if (x == 0):
            if (len(wpawncol[x]) == 1 and len(wpawncol[x+1]) == 0):
                heuristicscore += C.isolatedP #how bad an isolated pawn is
        elif (x == 7):
            if (len(wpawncol[x]) == 1 and len(wpawncol[x-1]) == 0):
                heuristicscore += C.isolatedP
        else: 
            if (len(wpawncol[x + 1]) == 0 and len(wpawncol[x - 1]) == 0):
                heuristicscore += C.isolatedP
        
        for y in wpawncol[x]:
            #checks if there are any passed pawns
            if (x == 0):
                if ((len(bpawncol[0]) == 0 or y >= bpawncol[0][len(bpawncol[0])-1]) and (len(bpawncol[1]) == 0 or y >= bpawncol[1][len(bpawncol[1])-1])):
                    heuristicscore += C.passedP #how good it is to have a passed pawn
            elif (x == 7):
                if ((len(bpawncol[6]) == 0 or y >= bpawncol[6][len(bpawncol[6])-1]) and (len(bpawncol[7]) == 0 or y >= bpawncol[7][len(bpawncol[7])-1])):
                    heuristicscore += C.passedP
            else:
                if ((len(bpawncol[x]) == 0 or y >= bpawncol[x][len(bpawncol[x])-1]) and (len(bpawncol[x-1]) == 0 or y >= bpawncol[x-1][len(bpawncol[x - 1])-1]) and (len(bpawncol[x+1]) == 0 or y >= bpawncol[x+1][len(bpawncol[x + 1])-1])):
                    heuristicscore += C.passedP
                    

            #checks if pawns are diagonal to each other
            if (x - 1 >= 0):
                if (y + 1 <= 7):
                    if(grid[x-1][y+1] == 'P'):
                        heuristicscore += C.diagP #how good pawns are to be diagonal
                if (y - 1 >= 0):
                    if(grid[x-1][y-1] == 'P'):
                        heuristicscore += C.diagP
            if (x + 1 <= 7):
                if (y + 1 <= 7):
                    if(grid[x+1][y+1] == 'P'):
                        heuristicscore += C.diagP
                if (y - 1 >= 0):
                    if(grid[x+1][y-1] == 'P'):
                        heuristicscore += C.diagP

    return heuristicscore

def heuristic(board, side): #side is the side "you" are playing as in the heuristic. The half heuristic is run for both sides and the difference is the final output
    if (board.is_game_over()):
        return overeval(board, side)
    if (side == chess.WHITE):
        return halfheuristic(board) - halfheuristic(board.mirror())
    return halfheuristic(board.mirror()) - halfheuristic(board)
def overeval(board, side): #only to be called when the board position in over. returns 0 if draw, inf if you won, -inf if you lost
    if (board.is_variant_draw()):
        return 0
    if (board.is_variant_win()):
        if (board.turn == side):
            return float("inf")
        return -float("inf")
    if (board.turn == side):
        return -float("inf")
    return float("inf")