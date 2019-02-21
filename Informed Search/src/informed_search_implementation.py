######################## Library definitions ########################
from copy import deepcopy
import numpy as np
import sys
import time

######################## Definition of class State ########################
class State:
    def __init__(self, start, parent=None):
        '''
            Initialise the state with f, g and h values = 0.
        '''
        self.board = start
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def goal_state(self):
        '''
            Check whether the current board is the goal state.
            Return either True or False.
            Goal state is:
                [0, 1, 2]
                [3, 4, 5]
                [6, 7, 8]
        '''
        value = 0
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] != value:
                    return False
                value += 1
        return True 

    def manhattan_distance(self):
        '''
            Compute the Manhattan distance of the current board.
            Manhattan distance: can only move in up, down, left 
            and right directions.
        '''
        heur = 0
        for index_i in range(self.board.shape[0]):
            for index_j in range(self.board.shape[1]):
                board_x, board_y = divmod(self.board[index_i][index_j], 3)
                heur += abs(board_x - index_i) + abs(board_y - index_j)
        return heur

    def misplaced_tiles_distance(self):
        '''
            Compute the misplaced tiles distance of the current  
            board.
            Misplaced tile distance: Total number of tiles that
            are in the incorrect position with respect to goal.
        '''
        value = 0
        heur = 0
        for index_i in range(self.board.shape[0]):
            for index_j in range(self.board.shape[1]):
                if self.board[index_i][index_j] != value%9:
                    heur += 1
            value += 1
        return heur

######################## Movement of the 'zero' tile ########################
def zero_movement(curr):
    '''
        Function to move the empty tile around the board.
    '''
  
    ## Estimate the location of the 'zero' tile
    for index_i in range(curr.board.shape[0]):
        for index_j in range(curr.board.shape[1]):
            if curr.board[index_i][index_j] == 0:
                zero_x, zero_y = index_i, index_j
                break

    queue = []

    '''
        Check the individual conditions for movement of tile,
        and append all possible states to the queue.
    '''
    ## UP movement possibility
    if zero_x - 1 >= 0:
        child = deepcopy(curr.board)
        child[zero_x][zero_y] = child[zero_x-1][zero_y]
        child[zero_x-1][zero_y] = 0
        child_state = State(child, curr.board)
        queue.append(child_state)

    ## DOWN movement possibility
    if zero_x + 1 < curr.board.shape[0]:
        child = deepcopy(curr.board)
        child[zero_x][zero_y] = child[zero_x+1][zero_y]
        child[zero_x+1][zero_y] = 0
        child_state = State(child, curr.board)
        queue.append(child_state)

    ## LEFT movement possibility
    if zero_y - 1 >= 0:
        child = deepcopy(curr.board)
        child[zero_x][zero_y] = child[zero_x][zero_y-1]
        child[zero_x][zero_y-1] = 0
        child_state = State(child, curr.board)
        queue.append(child_state)

    ## RIGHT movement possibility    
    if zero_y + 1 < curr.board.shape[1]:
        child = deepcopy(curr.board)
        child[zero_x][zero_y] = child[zero_x][zero_y+1]
        child[zero_x][zero_y+1] = 0
        child_state = State(child, curr.board)
        queue.append(child_state)

    return queue

######################## Estimation of least f(n) = g(n) + h(n) ########################
def leastfnvalue_estimate(open_list):
    '''
       Computes the next state to be expanded from the open list.
       Returns the state and the index in the open list, so that 
       this node can be popped off the open list later on.
    '''
    current_f = open_list[0].f
    current_index = 0
    for i, item in enumerate(open_list):
        if(item.f < current_f):
            current_f = item.f
            current_index  = i
    
    return open_list[current_index], current_index

######################## A* Algorithm ########################
def astar_solve(start, heuristic=None):
    open_list = []
    closed_list = []
    heuristic_mode = heuristic
    open_list.append(start)

    while open_list:
        current, index = leastfnvalue_estimate(open_list)

        if current.goal_state():
            return current, open_list, closed_list

        open_list.pop(index)
        closed_list.append(current)

        ## Get the children states.
        children_states = zero_movement(current)
        
        for child_state in children_states:
            closed_flag = 0 
            present_flag = 0
            
            ## Check whether current child state is already in the closed state.
            ##     If yes, discard this state, and check next child state.
            for closed_state in closed_list:
                if child_state == closed_state:
                    closed_flag = 1
                    break
        
            if not closed_flag:
                new_g = current.g + 1 
                
            ## Check whether current child state is already in the open state.
            ##     If yes, check whether already open state has a larger g value. 
            ##         If yes, update g and f values of already open state.
                for j, open_state in enumerate(open_list):
                    if child_state == open_state:
                        present_flag = 1
                        if new_g < open_list[j].g:
                            open_list[j].g = new_g
                            open_list[j].f = open_list[j].g + open_list[j].h
                            open_list[j].parent = current
        
                if not present_flag:
                    if (heuristic_mode.lower() == 'manhattan'):
                        child_state.g = new_g
                        child_state.h = child_state.manhattan_distance()
                        child_state.f = child_state.g + child_state.h
                        child_state.parent = current
                    elif (heuristic_mode.lower() == 'misplaced_tiles'):
                        child_state.g = new_g
                        child_state.h = child_state.misplaced_tiles_distance()
                        child_state.f = child_state.g + child_state.h
                        child_state.parent = current
                    open_list.append(child_state)
    return None, open_list, closed_list

######################## Greedy Algorithm ########################
def greedy_solve(start, heuristic=None):
    open_list = []
    closed_list = []
    heuristic_mode = heuristic
    open_list.append(start)

    while open_list:
        current, index = leastfnvalue_estimate(open_list)

        if current.goal_state():
            return current, open_list, closed_list

        open_list.pop(index)
        closed_list.append(current)

        ## Get the children states.
        children_states = zero_movement(current)
        
        for child_state in children_states:
            closed_flag = 0 
            present_flag = 0
            
            ## Check whether current child state is already in the closed state.
            ##     If yes, discard this state, and check next child state.
            for closed_state in closed_list:
                if child_state == closed_state:
                    closed_flag = 1
                    break
        
            if not closed_flag:
                new_f = current.f + 1 
                
                ## Check whether current child state is already in the open state.
                ##     If yes, check whether already open state has a larger g value. 
                ##         If yes, update g and f values of already open state.
                for j, open_state in enumerate(open_list):
                    if child_state == open_state:
                        present_flag = 1
                        if new_f < open_list[j].f:
                            open_list[j].f = open_list[j].h
                            open_list[j].parent = current
        
                if not present_flag:
                    if (heuristic_mode.lower() == 'manhattan'):
                        child_state.f = child_state.manhattan_distance()
                        child_state.parent = current
                    elif (heuristic_mode.lower() == 'misplaced_tiles'):
                        child_state.f = child_state.misplaced_tiles_distance()
                        child_state.parent = current
                    open_list.append(child_state)
    return None, open_list, closed_list

######################## Main - Greedy Algorithm ########################
def main_greedy(start, heuristic):
    '''
       Main function for Greedy Algorithm
    '''
    print("Solving puzzle: \n{} \n using Greedy Algorithm using heuristic function: {}\n"
           .format(puzzle, heuristic.upper()))
    
    time_start_greedy = time.time()
    result, open_list, closed_list = greedy_solve(start, heuristic)
    time_end_greedy = time.time()    

    num_of_moves = 0
    seq_of_moves = []

    solution = result.parent
    while solution:
        num_of_moves += 1
        seq_of_moves.append(solution.board)
        solution = solution.parent

    print ("Details of execution:\n=========================================")
    print ("Number of moves required: {}\nCost of reaching goal state: {}\nTime required: {:.6f} seconds"
            .format(num_of_moves, result.f, time_end_greedy - time_start_greedy))
    print ("Number of nodes in fringe: {}\nNumber of nodes visited: {}"
            .format(len(open_list), len(closed_list)))
    print ("Steps taken for solution:")
    for solution in reversed(seq_of_moves):
        print (solution)
        print ("    |")
        print ("    V")
    print (result.board)

######################## Main - A* Algorithm ########################
def main_astar(start, heuristic):
    '''
       Main function for A* Algorithm
    '''
    print("Solving puzzle: \n{} \n using A* algorithm using heuristic function: {}\n"
          .format(puzzle, heuristic.upper()))

    time_start_astar = time.time()
    result, open_list, closed_list = astar_solve(start, heuristic)
    time_end_astar = time.time()    
    
    num_of_moves = 0
    seq_of_moves = []

    solution = result.parent
    while solution:
        num_of_moves += 1
        seq_of_moves.append(solution.board)
        solution = solution.parent

    print ("Details of execution:\n=========================================")
    print ("Number of moves required: {}\nCost of reaching goal state: {}\nTime required: {:.6f} seconds"
            .format(num_of_moves, result.g, time_end_astar - time_start_astar))
    print ("Number of nodes in fringe: {}\nNumber of nodes visited: {}"
           .format(len(open_list), len(closed_list)))
    print ("Steps taken for solution:")
    for solution in reversed(seq_of_moves):
        print (solution)
        print ("    |")
        print ("    V")
    print (result.board)

######################## Main method ########################
if __name__ == '__main__':

############ Puzzles ############
#    puzzle = np.array([[8, 7, 6],
#                       [5, 1, 4],
#                       [2, 0, 3]])
    puzzle = np.array([[1, 4, 2],
                       [3, 7, 5],
                       [6, 0, 8]])
#    puzzle = np.array([[5, 2, 8],
#                       [4, 1, 7],
#                       [0, 3, 6]])
#    puzzle = np.array([[1, 4, 2],
#                       [3, 5, 0],
#                       [6, 7, 8]])
#    puzzle = np.array([[1, 0, 2],
#                       [3, 4, 5],
#                       [6, 7, 8]])
##################################
    
    start = State(puzzle)

    heuristic = sys.argv[-1]

    main_greedy(start, heuristic)
    print("\n==================================================================================\n")
    main_astar(start, heuristic)
    
