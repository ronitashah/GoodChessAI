import chess
def halfhuerestic(board): #should run the huerestic from whites percpective and look primarly at white's things(like only white's material and stuff)
    return 0

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