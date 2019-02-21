'''
    Creation of a puzzle object through class Puzzle
'''

class Puzzle(object):

    # Number of rows and columns in the board
    ROWS = 6
    COLS = 7

    def __init__(self, original_board=None):

        # If board already exists - used for creation of child_board boards
        if(original_board):
            self.game = [list(col) for col in original_board.game]
            self.num_moves = original_board.num_moves
            self.last_move = original_board.last_move

        # Creation of a new board
        else:          
            self.game = [[] for x in range(self.COLS)]
            self.num_moves = 0
            self.last_move = None
        
    def fill_puzzle(self, column):
        '''
            Function to fill the board with 'X' or 'O'
        '''
        piece = self.num_moves % 2
        self.last_move = (piece, column)
        self.num_moves += 1
        self.game[column - 1].append(piece)

    def child_board(self):
        '''
            Function to create child_board of the board
            Returns (moves_needed, child_board)
        '''
        child_board = []
        for i in range(1, self.COLS + 1):
            if len(self.game[i - 1]) < self.ROWS:
                child = Puzzle(self)
                child.fill_puzzle(i)
                child_board.append((i, child))
        return child_board

    def check_puzzle_solved(self):
        '''
            Function to check whether board has been solved or not
            Returns the following values:
                0 - Draw if all the tiles are filled in
                1 - Player 1 has won
                2 - Player 2 has won
                -1 - Game continues, no player has won yet
        '''
        for i in range(0,self.COLS):
            for j in range(0,self.ROWS):
                try:
                    # Check for horizontal streak - COL wise 4 in a row
                    if self.game[i][j]  == self.game[i + 1][j] == self.game[i + 2][j] == self.game[i + 3][j]:
                        return self.game[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Check for vertical streak - ROW wise 4 in a row
                    if self.game[i][j]  == self.game[i][j + 1] == self.game[i][j + 2] == self.game[i][j + 3]:
                        return self.game[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Check for diagonal streak - positive slope 4 in a row
                    if not j + 3 > self.ROWS and \
                       self.game[i][j] == self.game[i + 1][j + 1] == self.game[i + 2][j + 2] == self.game[i + 3][j + 3]:
                        return self.game[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Check for diagonal streak - negative slope 4 in a row
                    if not j - 3 < 0 and \
                       self.game[i][j] == self.game[i + 1][j - 1] == self.game[i + 2][j - 2] == self.game[i + 3][j - 3]:
                        return self.game[i][j] + 1
                except IndexError:
                    pass

        # If all the cells have been filled in 
        if self.num_moves == self.ROWS * self.COLS:
            return 0

        return -1

    def show_game(self):
        '''
            Function to print the board to the console
        '''
        print ("")
        print (" " + "--- " * self.COLS)
        for rows in range(self.ROWS - 1, -1, -1):
            row = "|"
            for cols in range(self.COLS):
                if len(self.game[cols]) > rows:
                    # 'X' signifies player 1; 'O' signifies player 2
                    row += " " + ('X' if self.game[cols][rows] else 'O') + " |"
                else:
                    row += "   |"
            print(row)
            print(" " + "--- " * self.COLS)
        print ("  1   2   3   4   5   6   7")
        print ("Last move: COLUMN {}\t".format(self.last_move[1])),
        print ("Total moves: {}".format(self.num_moves))
        print ("")
    
