import argparse
import copy
import sys
import time

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):
        self.board = board

        self.width = 8
        self.height = 8

        # init with red player's turn
        # self.turn = 'r'

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

def deepcopy_move_diagonally_and_return_new_state(state, row, col, new_row, new_col):
    """
    Move diagonally one square
    """
    new_board = copy.deepcopy(state.board)
    new_board[new_row][new_col] = new_board[row][col]
    new_board[row][col] = '.'

    # if the piece reaches the end of the board, become a king
    if new_row == 0 and new_board[new_row][new_col] == 'r':
        new_board[new_row][new_col] = 'R'
    elif new_row == 7 and new_board[new_row][new_col] == 'b':
        new_board[new_row][new_col] = 'B'

    new_state = State(new_board)
    # new_state.turn = get_next_turn(state.turn)
    return new_state

def nested_list_to_only_elements(nested_list):
    """
    Recursively turns a nested list to a list of just the elements
    """
    element_list = []
    for element in nested_list:
        if isinstance(element, list):
            element_list.extend(nested_list_to_only_elements(element))
        else:
            element_list.append(element)
    return element_list

def deepcopy_jump_recursively_and_return_new_state(state, row, col, new_row, new_col, curr_turn):
    """
    Keeps jumping diagonally until it can't
    """
    new_successor_states = []
    new_board = copy.deepcopy(state.board)

    # initial jump from row, col to new_row, new_col
    new_board[new_row][new_col] = new_board[row][col]
    new_board[row][col] = '.'

    # remove the piece that was jumped over
    if new_row < row and new_col < col:
        new_board[row-1][col-1] = '.'
    elif new_row < row and new_col > col:
        new_board[row-1][col+1] = '.'
    elif new_row > row and new_col < col:
        new_board[row+1][col-1] = '.'
    elif new_row > row and new_col > col:
        new_board[row+1][col+1] = '.'

    # if the piece reaches the end of the board, become a king and end the jump
    if new_row == 0 and new_board[new_row][new_col] == 'r':
        new_board[new_row][new_col] = 'R'
        new_state = State(new_board)
        # new_state.turn = get_next_turn(state.turn)
        return new_state
    elif new_row == 7 and new_board[new_row][new_col] == 'b':
        new_board[new_row][new_col] = 'B'
        new_state = State(new_board)
        # new_state.turn = get_next_turn(state.turn)
        return new_state

    # check if piece at new_row, new_col can jump left or right
    if curr_turn == 'r':
        # check if new r piece can jump left
        if (new_row-2 >= 0) and (new_col-2 >= 0) and new_board[new_row-1][new_col-1] in get_opp_char(curr_turn) and new_board[new_row-2][new_col-2] == '.':
            # print("JUMP FORWARDS LEFT")
            # new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row-2, new_col-2, get_next_turn(curr_turn)))
            new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row-2, new_col-2, "r"))

        # check if new r piece can jump right
        if (new_row-2 >= 0) and (new_col+2 < 8) and new_board[new_row-1][new_col+1] in get_opp_char(curr_turn) and new_board[new_row-2][new_col+2] == '.':
            # print("JUMP FORWARDS RIGHT")
            # print("JUMPING FROM ", new_row, new_col, " TO ", new_row-2, new_col+2)
            new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row-2, new_col+2, "r"))
        
        if new_board[new_row][new_col] == 'R':
            
            # check if new R piece can backwards jump left
            if (new_row+2 < 8) and (new_col-2 >= 0) and new_board[new_row+1][new_col-1] in get_opp_char(curr_turn) and new_board[new_row+2][new_col-2] == '.':
                # print("JUMP BACKWARDS LEFT")
                new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row+2, new_col-2, "r"))
            
            # check if new R piece can backwards jump right
            if (new_row+2 < 8) and (new_col+2 < 8) and new_board[new_row+1][new_col+1] in get_opp_char(curr_turn) and new_board[new_row+2][new_col+2] == '.': 
                # print("JUMP BACKWARDS RIGHT")
                new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row+2, new_col+2, "r"))

    elif curr_turn == 'b':
        # check if new b piece can jump left
        if (new_row+2 < 8) and (new_col-2 >= 0) and new_board[new_row+1][new_col-1] in get_opp_char(curr_turn) and new_board[new_row+2][new_col-2] == '.': 
            new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row+2, new_col-2, "b"))
        
        # check if new b piece can jump right
        if (new_row+2 < 8) and (new_col+2 < 8) and new_board[new_row+1][new_col+1] in get_opp_char(curr_turn) and new_board[new_row+2][new_col+2] == '.':
            new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row+2, new_col+2, "b"))

        if new_board[new_row][new_col] == 'B':
            # check if new B piece can backwards jump left
            if (new_row-2 >= 0) and (new_col-2 >= 0) and new_board[new_row-1][new_col-1] in get_opp_char(curr_turn) and new_board[new_row-2][new_col-2] == '.':
                new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row-2, new_col-2, "b"))
            
            # check if new B piece can backwards jump right
            if (new_row-2 >= 0) and (new_col+2 < 8) and new_board[new_row-1][new_col+1] in get_opp_char(curr_turn) and new_board[new_row-2][new_col+2] == '.':
                new_successor_states.append(deepcopy_jump_recursively_and_return_new_state(State(new_board), new_row, new_col, new_row-2, new_col+2, "b"))

    # if piece can't jump anymore, return new state after 1 jump, else return set of successor states
    if len(new_successor_states) == 0:
        # print("PRINT NEW BOARD:")
        new_state = State(new_board)
        # new_state.turn = get_next_turn(state.turn)
        return new_state
    else:
        result = nested_list_to_only_elements(new_successor_states)
        return result

def add_to_list(list_, item):
    # if isinstance(item, list):
    #     list_.extend(item)
    if isinstance(item[1], list):
        for succ in item[1]:
            list_.append((item[0],succ))
    else:
        list_.append(item)

def generate_successors(state, curr_turn):
    '''
    Takes in a state
    Returns a list of successtors to that current state
    '''
    board = state.board
    # curr_turn = state.turn
    
    # new_successor_states contains the list of successor states in a tuple (isJump, new_state) 
    new_successor_states = []

    for row in range(len(board)):
        for col in range(len(board[row])):
            # check if the current player can jump
            canJump = False

            # if red's turn and the piece is red
            if curr_turn == 'r' and board[row][col] in ['r', 'R']:

                # check if piece can jump diagonally left
                if (row-2 >= 0) and (col-2 >= 0) and board[row-1][col-1] in get_opp_char(curr_turn) and board[row-2][col-2] == '.':
                    # print("PIECE:" , board[row][col], "CAN JUMP LEFT")
                    # print("PIECE COORDINATES:", row, col)
                    new_succ = deepcopy_jump_recursively_and_return_new_state(state, row, col, row-2, col-2, "r")
                    add_to_list(new_successor_states, (True, new_succ))
                    canJump = True

                # check if piece can jump diagonally right
                if (row-2 >= 0) and (col+2 < 8) and board[row-1][col+1] in get_opp_char(curr_turn) and board[row-2][col+2] == '.':
                    new_succ = deepcopy_jump_recursively_and_return_new_state(state, row, col, row-2, col+2, "r")
                    add_to_list(new_successor_states, (True, new_succ))
                    canJump = True
                
                if board[row][col] == "R":
                    # check if piece can jump backwards diagonally left
                    if (row+2 < 8) and (col-2 >= 0) and board[row+1][col-1] in get_opp_char(curr_turn) and board[row+2][col-2] == '.': 
                        # print("INITIAL JUMP BACKWARDS LEFT")
                        new_succ = deepcopy_jump_recursively_and_return_new_state(state, row, col, row+2, col-2, "r")
                        add_to_list(new_successor_states, (True, new_succ))
                        canJump = True
                    
                    # check if piece can jump backwards diagonally right
                    if (row+2 < 8) and (col+2 < 8) and board[row+1][col+1] in get_opp_char(curr_turn) and board[row+2][col+2] == '.':
                        # print("INITIAL JUMP BACKWARDS RIGHT")
                        new_succ = deepcopy_jump_recursively_and_return_new_state(state, row, col, row+2, col+2, "r")
                        add_to_list(new_successor_states, (True, new_succ))
                        canJump = True

                # check if piece can move diagonally left
                if canJump == False and (row-1 >= 0) and (col-1 >= 0) and board[row-1][col-1] == '.':
                    add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row-1, col-1)))
                
                # check if piece can move diagonally right
                if canJump == False and (row-1 >= 0) and (col+1 < 8) and board[row-1][col+1] == '.':
                    add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row-1, col+1)))
                
                # check if piece is a king
                if board[row][col] == 'R':
                    
                    # check if piece can move backwards diagonally left
                    if canJump == False and (row+1 < 8) and (col-1 >= 0) and board[row+1][col-1] == '.':
                        add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row+1, col-1)))
                    
                    # check if piece can move backwards diagonally right
                    if canJump == False and (row+1 < 8) and (col+1 < 8) and board[row+1][col+1] == '.':
                        add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row+1, col+1)))
                    
            elif curr_turn == 'b' and board[row][col] in ['b', 'B']:
                # check if piece can jump diagonally left
                if (row+2 < 8) and (col-2 >= 0) and board[row+1][col-1] in get_opp_char(curr_turn) and board[row+2][col-2] == '.':
                    add_to_list(new_successor_states, (True, deepcopy_jump_recursively_and_return_new_state(state, row, col, row+2, col-2, "b")))
                    canJump = True

                # check if piece can jump diagonally right
                if (row+2 < 8) and (col+2 < 8) and board[row+1][col+1] in get_opp_char(curr_turn) and board[row+2][col+2] == '.':
                    add_to_list(new_successor_states, (True, deepcopy_jump_recursively_and_return_new_state(state, row, col, row+2, col+2, "b")))
                    canJump = True
                
                if board[row][col] == 'B':
                    # check if piece can jump backwards diagonally left
                    if (row-2 >= 0) and (col-2 >= 0) and board[row-1][col-1] in get_opp_char(curr_turn) and board[row-2][col-2] == '.':
                        add_to_list(new_successor_states, (True, deepcopy_jump_recursively_and_return_new_state(state, row, col, row-2, col-2, "b")))
                        canJump = True
                    
                    # check if piece can jump backwards diagonally right
                    if (row-2 >= 0) and (col+2 < 8) and board[row-1][col+1] in get_opp_char(curr_turn) and board[row-2][col+2] == '.':
                        add_to_list(new_successor_states, (True, deepcopy_jump_recursively_and_return_new_state(state, row, col, row-2, col+2, "b")))
                        canJump = True

                # check if piece can move diagonally left
                if canJump == False and (row+1 < 8) and (col-1 >= 0) and board[row+1][col-1] == '.':
                    add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row+1, col-1)))
                
                # check if piece can move diagonally right
                if canJump == False and (row+1 < 8) and (col+1 < 8) and board[row+1][col+1] == '.':
                    add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row+1, col+1)))
                
                # check if piece is a king
                if board[row][col] == 'B':
                    # check if piece can move backwards diagonally left
                    if canJump == False and (row-1 >= 0) and (col-1 >= 0) and board[row-1][col-1] == '.': 
                        add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row-1, col-1)))
                    
                    # check if piece can move backwards diagonally right
                    if canJump == False and (row-1 >= 0) and (col+1 < 8) and board[row-1][col+1] == '.':
                        add_to_list(new_successor_states, (False, deepcopy_move_diagonally_and_return_new_state(state, row, col, row-1, col+1)))

    hasJump = False
    for successor in new_successor_states:
        if successor[0] == True:
            hasJump = True
            break
    
    final_successor_states = []
    if hasJump == True:
        for successor in new_successor_states:
            if successor[0] == True:
                final_successor_states.append(successor[1])
    else:
        for successor in new_successor_states:
            final_successor_states.append(successor[1])

    return final_successor_states

def return_utility(state):

    exists_red_piece = False
    exists_black_piece = False

    for row in state.board:
        for piece in row:
            if exists_red_piece and exists_black_piece:
                break

            if piece in ['r', 'R']:
                exists_red_piece = True
            elif piece in ['b', 'B']:
                exists_black_piece = True
    
    if not exists_red_piece:
        return -1000000000 
    elif not exists_black_piece:
        return 1000000000
    else:
        return return_non_terminal_utility(state)

def return_non_terminal_utility(state):

    num_red_normal_pieces = 0
    num_black_normal_pieces = 0

    num_red_king_pieces = 0
    num_black_king_pieces = 0

    row_counter = 7
    for row in state.board:
        for piece in row:
            if piece == 'r':
                num_red_normal_pieces += (1 + row_counter)
            elif piece == 'b':
                num_black_normal_pieces += (1 + (7 - row_counter))
            elif piece == 'R':
                num_red_king_pieces += 1
            elif piece == 'B':
                num_black_king_pieces += 1
            
        row_counter -= 1
            
            
    
    simple_eval = (12*num_red_king_pieces + num_red_normal_pieces) - (12*num_black_king_pieces + num_black_normal_pieces)
    
    return simple_eval

def alphabeta_search(state, depth_limit, curr_turn):
    v = alphabeta_max_node(state, curr_turn, -2000000000, 2000000000, depth_limit)

    return v[1]

# cache is a dictionary
cached = {} # you can use this to implement state caching!
# cached = {state: (value v, depth, successor)}

def alphabeta_max_node(state, turn, alpha, beta, current_depth):
    if state in cached and cached[state][1] >= current_depth:
        return (cached[state][0], cached[state][2])
    
    if current_depth == 0:
        return (return_utility(state), None)

    successors = generate_successors(state, turn)

    if len(successors) == 0:
        cached[state] = (-1000000000, current_depth, None)
        return (-1000000000, None)

    # sort successors by utility function
    successors.sort(key=lambda x: return_utility(x), reverse=True)

    v = -2000000000
    best = state

    for child in successors:

        tempval, tempstate = alphabeta_min_node(child, get_next_turn(turn), alpha, beta, current_depth-1)

        if tempval > v:
            v = tempval
            best = child
        
        if tempval > beta:
            cached[state] = (v, current_depth, child)
            return (v, child)
        
        alpha = max(alpha, tempval)
        cached[state] = (v, current_depth, best)
    
    return (v, best)

def alphabeta_min_node(state, turn, alpha, beta, current_depth):
    if state in cached and cached[state][1] >= current_depth:
        return (cached[state][0], cached[state][2])
    
    if current_depth == 0:
        return (return_utility(state), None)

    successors = generate_successors(state, turn)

    if len(successors) == 0:
        cached[state] = (1000000000, current_depth, None)
        return (1000000000, None)

    # sort successors by utility function
    successors.sort(key=lambda x: return_utility(x), reverse=False)

    v = 2000000000
    best = state

    for child in successors:

        tempval, tempstate = alphabeta_max_node(child, get_next_turn(turn), alpha, beta, current_depth-1)

        if tempval < v:
            v = tempval
            best = child
        
        if tempval < alpha:
            cached[state] = (v, current_depth, child)
            return (v, child)
        
        beta = min(beta, tempval)
        cached[state] = (v, current_depth, best)
    
    return (v, best)
    
def get_curr_char(player):
    if player in ['b', 'B']:
        return ['b', 'B']
    else:
        return ['r', 'R']
        
def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    turn = 'r'
    depth_limit = 8
    ctr = 0

    # Main Checkers Game Loop with Alpha Beta Pruning
    
    start_time = time.time()

    sys.stdout = open(args.outputfile, 'w')

    state.display()
    while return_utility(state) < 1000000000:
        new_state = alphabeta_search(state, depth_limit, turn)
        turn = get_next_turn(turn)
        new_state.display()
        state = new_state

    sys.stdout = sys.__stdout__

    end_time = time.time()
    print("TIME ELAPSED: " + str(end_time - start_time))

    

