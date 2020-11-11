import chess
def halfhuerestic(board): #should run the huerestic from whites percpective and look primarly at white's things(like only white's material and stuff)
    grid = [['' for i in range(8)] for j in range(8)]
    for y in range(8):
        for x in range(8):
            piece = board.piece_at(chess.SQUARES[y + 8*x])
            if (temp == None):
                grid[x][y] = ' '
            else:
                grid[x][y] = piece.piece_type()

def huerestic(board, side): #side is the side "you" are playing as in the huerestic. The half huerestic is run for both sides and the difference is the final output
    if (board.is_game_over()):
        return overeval(board, side)
    if (side == chess.WHITE):
        return halfhuerestic(board) - halfhuerestic(board.mirror())
    return halfhuerestic(board.mirror()) - halfhuerestic(board)
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