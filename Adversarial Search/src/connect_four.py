'''
    Creation of main class ConnectFour for implementing functionalities of 
    helper classes, namely, Puzzle and HumanPlayer, MiniMaxPlayer and
    AlphaBetaPruningPlayer
'''

from puzzle import Puzzle
from player_types import HumanPlayer, MiniMaxPlayer, AlphaBetaPruningPlayer

class ConnectFour:

    def __init__(self, start_puzzle, player_one, player_two):
        self.start_puzzle = start_puzzle
        self.player_one = player_one
        self.player_two = player_two

    def start_game(self):

        starting_player = self.player_one.start
        
        while(True):

            # Check whether human player starts
            if (starting_player == True):
                move = self.player_one.make_move(self.start_puzzle)
            else:
                move = self.player_two.make_move(self.start_puzzle)

            # Based on the player's turn, fill the puzzle, then show it
            self.start_puzzle.fill_puzzle(move)
            self.start_puzzle.show_game()

            # Check whether game is over
            # If not, switch player and continue the loop
            check_game_state = self.start_puzzle.check_puzzle_solved()
            if check_game_state == 0:
                print ("It is a draw!")
                break
            elif check_game_state == 1:
                print ("Player 1 wins!")
                break
            elif check_game_state == 2:
                print ("Player 2 wins!")
                break
            starting_player = not(starting_player)

if __name__ == "__main__":
    user_choice = input("\nWelcome to Connect Four!!\nChoose your opponent (1 or 2):\n1. MiniMax Player\t2. AlphaBetaPruning Player: ")
    while (True):
        if (user_choice == 1):
            game = ConnectFour(Puzzle(), HumanPlayer(start=True), MiniMaxPlayer(depth=5))
            break
        elif (user_choice == 2):
            game = ConnectFour(Puzzle(), HumanPlayer(start=True), AlphaBetaPruningPlayer(depth=5))
            break
        else: 
            print ("\nInvalid choice. Please select option 1 or 2.")
            user_choice = input("\nWelcome to Connect Four!!\nChoose your opponent (1 or 2):\n1. MiniMax Player\t2. AlphaBetaPruning Player: ")

    game.start_game()
