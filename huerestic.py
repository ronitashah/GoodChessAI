import chess
def halfhuerestic(board): #should run the huerestic from whites percpective and look primarly at white's things(like only white's material and stuff)
    return 0
def huerestic(board, side): #side is the side "you" are playing as in the huerestic. The half huerestic is run for both sides and the difference is the final output
    if (side == chess.WHITE):
        return halfhuerestic(board) - halfhuerestic(board.mirror())
    return halfhuerestic(board.mirror()) - halfhuerestic(board)