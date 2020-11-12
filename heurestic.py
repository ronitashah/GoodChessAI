import chess
def halfheurestic(board): #should run the heurestic from whites percpective and look primarly at white's things(like only white's material and stuff)
    heuristicscore = 0
    #grid setup to represent the board
    grid = [['' for i in range(8)] for j in range(8)]
    for y in range(8):
        for x in range(8):
            piece = board.piece_at(chess.SQUARES[y + 8*x])
            if (piece == None):
                grid[x][y] = ' '
            else:
                grid[x][y] = piece.symbol()

    #checks if pawns are diagonal to each other
    for y in range(8):
        for x in range(8):
            if (grid[x][y] == 'P'):
                if (x - 1 >= 0):
                    if (y + 1 <= 7):
                        if(grid[x-1][y+1] == 'P'):
                            heuristicscore += 1
                    if (y - 1 >= 0):
                        if(grid[x-1][y-1] == 'P'):
                            heuristicscore += 1
                if (x + 1 <= 7):
                    if (y + 1 <= 7):
                        if(grid[x+1][y+1] == 'P'):
                            heuristicscore += 1
                    if (y - 1 >= 0):
                        if(grid[x+1][y-1] == 'P'):
                            heuristicscore += 1
    return heuristicscore

def heurestic(board, side): #side is the side "you" are playing as in the heurestic. The half heurestic is run for both sides and the difference is the final output
    if (board.is_game_over()):
        return overeval(board, side)
    if (side == chess.WHITE):
        return halfheurestic(board) - halfheurestic(board.mirror())
    return halfheurestic(board.mirror()) - halfheurestic(board)
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