import math

from puzzle import Puzzle

class MiniMaxPlayer():
    def __init__(self, depth):
        self.depthLimit = depth

    def evaluation_function(self, board):
        '''
            Function to estimate value of a given board
            Calculates the cost of both the players based on the number of 
            favourable pieces present as follows:
                2 in a row - +-100
                3 in a row - +-10000
                4 in a row - +-1000000
        '''
        eval_value = 0
        state = board.game
        for i in range(0, board.COLS):
            for j in range(0, board.ROWS):
                # Check for horizontal streaks for both player 1 and player 2
                try:
                    # add player one streak scores to eval_value
                    if state[i][j] == state[i + 1][j] == 0:
                        eval_value += 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 0:
                        eval_value += 10000
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 0:
                        eval_value += 1000000

                    # subtract player two streak score to eval_value
                    if state[i][j] == state[i + 1][j] == 1:
                        eval_value -= 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 1:
                        eval_value -= 10000
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for vertical streaks for both player 1 and player 2
                try:
                    # add player one vertical streaks to eval_value
                    if state[i][j] == state[i][j + 1] == 0:
                        eval_value += 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 0:
                        eval_value += 10000
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 0:
                        eval_value += 1000000

                    # subtract player two streaks from eval_value
                    if state[i][j] == state[i][j + 1] == 1:
                        eval_value -= 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 1:
                        eval_value -= 10000
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for diagonal streaks with negative slope for both player 1 and player 2
                try:
                    # add player one streaks to eval_value
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == 0:
                        eval_value += 100
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 0:
                        eval_value += 10000
                    if not j + 3 > board.ROWS and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 0:
                        eval_value += 1000000

                    # add player two streaks to eval_value
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == 1:
                        eval_value -= 100
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 1:
                        eval_value -= 10000
                    if not j + 3 > board.ROWS and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for diagonal streaks with negative slope for both player 1 and player 2
                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 0:
                        eval_value += 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 0:
                        eval_value += 10000
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 0:
                        eval_value += 1000000

                    # subtract player two streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 1:
                        eval_value -= 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 1:
                        eval_value -= 10000
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass
        return eval_value


    def make_move(self, board):
        '''
            Function to return the optimal move based on MiniMax algorithm
        '''
        score, move = self.miniMax(board, self.depthLimit)
        print("Move made by AI: COLUMN {}".format(move))
        return move

    def miniMax(self, board, depth):
        '''
            Function to implement MiniMax algorithm
        '''

        if board.check_puzzle_solved() == 0:
            return 9999999999, -1
        elif depth == 0:
            return self.evaluation_function(board), -1

        bestScore = 9999999999
        shouldReplace = lambda x: x < bestScore
        bestMove = -1

        children = board.child_board()
        for child in children:
            move, childboard = child
            temp = self.miniMax(childboard, depth-1)[0]
            if shouldReplace(temp):
                bestScore = temp
                bestMove = move
        return bestScore, bestMove

class AlphaBetaPruningPlayer():

    def __init__(self, depth):
        self.depthLimit = depth

    def evaluation_function(self, board):
        '''
            Function to estimate value of a given board
            Calculates the cost of both the players based on the number of 
            favourable pieces present as follows:
                2 in a row - +-100
                3 in a row - +-10000
                4 in a row - +-1000000
        '''
        eval_value = 0
        state = board.game
        for i in range(0, board.COLS):
            for j in range(0, board.ROWS):
                # Check for horizontal streaks for both player 1 and player 2
                try:
                    # add player one streak scores to eval_value
                    if state[i][j] == state[i + 1][j] == 0:
                        eval_value += 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 0:
                        eval_value += 10000
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 0:
                        eval_value += 1000000

                    # subtract player two streak score to eval_value
                    if state[i][j] == state[i + 1][j] == 1:
                        eval_value -= 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 1:
                        eval_value -= 10000
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for vertical streaks for both player 1 and player 2
                try:
                    # add player one vertical streaks to eval_value
                    if state[i][j] == state[i][j + 1] == 0:
                        eval_value += 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 0:
                        eval_value += 10000
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 0:
                        eval_value += 1000000

                    # subtract player two streaks from eval_value
                    if state[i][j] == state[i][j + 1] == 1:
                        eval_value -= 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 1:
                        eval_value -= 10000
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for diagonal streaks with negative slope for both player 1 and player 2
                try:
                    # add player one streaks to eval_value
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == 0:
                        eval_value += 100
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 0:
                        eval_value += 10000
                    if not j + 3 > board.ROWS and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 0:
                        eval_value += 1000000

                    # add player two streaks to eval_value
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == 1:
                        eval_value -= 100
                    if not j + 3 > board.ROWS and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 1:
                        eval_value -= 10000
                    if not j + 3 > board.ROWS and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass

                # Check for diagonal streaks with negative slope for both player 1 and player 2
                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 0:
                        eval_value += 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 0:
                        eval_value += 10000
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 0:
                        eval_value += 1000000

                    # subtract player two streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 1:
                        eval_value -= 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 1:
                        eval_value -= 10000
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 1:
                        eval_value -= 1000000
                except IndexError:
                    pass
        return eval_value

    def make_move(self, board):
        '''
            Function to return the optimal move based on AlphaBeta algorithm
        '''
        score, move = self.alphaBeta(board, self.depthLimit, -9999999999, 9999999999)
        print("Move made by AI: COLUMN {}".format(move))
        return move

    def alphaBeta(self, board, depth, alpha, beta):
        '''
            Function to implement AlphaBeta algorithm
        '''
        if board.check_puzzle_solved() == 0:
            return 9999999999, -1
        elif depth == 0:
            return self.evaluation_function(board), -1

        bestScore = 9999999999
        shouldReplace = lambda x: x < bestScore
        bestMove = -1

        children = board.child_board()
        for child in children:
            move, childboard = child
            temp = self.alphaBeta(childboard, depth-1, alpha, beta)[0]
            if shouldReplace(temp):
                bestScore = temp
                bestMove = move

            alpha = max(alpha, temp)
            beta = min(beta, temp)
            if alpha >= beta:
                break

        return bestScore, bestMove


class HumanPlayer():
    
    start = False

    def __init__(self, start=False):
        self.start = start

    def make_move(self, board):
        
        col = input("Make your move!\nEnter col value between 1 and 7: ")
        return col
