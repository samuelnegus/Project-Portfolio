import heapq

def state_check(state):
    """check the format of state, and return corresponding goal state.
       Do NOT edit this function."""
    non_zero_numbers = [n for n in state if n != 0]
    num_tiles = len(non_zero_numbers)
    if num_tiles == 0:
        raise ValueError('At least one number is not zero.')
    elif num_tiles > 9:
        raise ValueError('At most nine numbers in the state.')
    matched_seq = list(range(1, num_tiles + 1))
    if len(state) != 9 or not all(isinstance(n, int) for n in state):
        raise ValueError('State must be a list contain 9 integers.')
    elif not all(0 <= n <= 9 for n in state):
        raise ValueError('The number in state must be within [0,9].')
    elif len(set(non_zero_numbers)) != len(non_zero_numbers):
        raise ValueError('State can not have repeated numbers, except 0.')
    elif sorted(non_zero_numbers) != matched_seq:
        raise ValueError('For puzzles with X tiles, the non-zero numbers must be within [1,X], '
                          'and there will be 9-X grids labeled as 0.')
    goal_state = matched_seq
    for _ in range(9 - num_tiles):
        goal_state.append(0)
    return tuple(goal_state)

def get_manhattan_distance(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    goal_positions = {value: index for index, value in enumerate(to_state)}
    for i, value in enumerate(from_state):
        if value != 0: #Not counting the distance of tiles 0. 
            goal_pos = goal_positions[value]
            #To calculate the manhattan distance here, i // 3 gets the row of the 
            #current tile in from_state and goal_pos // 3 is the row of the same tile 
            #in the goal state. Similarly, i % 3 is the column of the current tile
            #in from_state and goal_pos % 3 is the column of the same tile in the goal state.
            distance += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3) 
    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """

    # given state, check state format and get goal_state.
    goal_state = state_check(state)
    # please remove debugging prints when you submit your code.
    # print('initial state: ', state)
    # print('goal state: ', goal_state)

    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state,goal_state)))

def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    #All valid moves for each tile location on a 3x3 grid. Each index is mapped to 
    #a list of indices that represents all neighbors of that index. 
    possible_moves = { 
        0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
        3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
        6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
    }
    #Tiles '0' are empty spaces.  
    empty_spaces = [i for i, value in enumerate(state) if value == 0]
    #Swapping tiles with empty spaces. 
    for space in empty_spaces:
        for move in possible_moves[space]:
            updated_state = state[:]
            updated_state[space], updated_state[move] = updated_state[move], updated_state[space] 
            if updated_state not in succ_states:  #Avoiding duplicates.
                succ_states.append(updated_state)

    return sorted(succ_states) #Successors sorted in ascending order.

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """

    # This is a format helper，which is only designed for format purpose.
    # define "solvable_condition" to check if the puzzle is really solvable
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute "max_length", it might be useful in debugging
    # it can help to avoid any potential format issue.

    # given state, check state format and get goal_state.
    goal_state = state_check(state)
    # please remove debugging prints when you submit your code.

    solvable_condition = True #Initializing as true. 
    visited = set() #Keeping a set of visited states to guarantee stopping in finite iterations. 

    pq = []
    heapq.heappush(pq, (0, state, (0, -1)))  #Pushing current state with priority 0, no moves made yet so cost is 0. Initial state -1 with no parent. 
    act_cost = {tuple(state):0} #Costs from starting node (g). 
    parent_state = {tuple(state):None}
    max_length = 0
    state_info_list = []

    #Checking solvability using the visited set. 
    if tuple(state) in visited:
        solvable_condition = False

    if not solvable_condition:
        print(False)
        return
    else:
        print(True)

    while pq:
        max_length = max(max_length, len(pq))
        _, current_state, (g, _) = heapq.heappop(pq) #Storing current state. 
        current_state_tuple = tuple(current_state)

        #If this state as already been visited, skip it.
        if current_state_tuple in visited:
            continue

        #Adding current state to list of visited. 
        visited.add(current_state_tuple)

        #If the goal state is reached, puzzle is solved. 
        if current_state == list(goal_state):
            current = current_state_tuple #Setting to the tuple version to trace back the path. 
            num_moves = g #G is the number of moves to the goal state. 
            while current is not None: #Looping until intial state. 
                h = get_manhattan_distance(list(current), goal_state) #heuristic value
                state_info_list.append((list(current), h, num_moves)) #Adding current state info to solution path. 
                current = parent_state[current] #Updating to parent state. 
                num_moves -= 1 #Backtracking through the path. 
            state_info_list.reverse() #From goal state to intial state, so needs to be reversed to be from initial state to goal state. Breaking when the goal state is reached and solution path is fully constructed. 
            break

        for neighbor in get_succ(current_state): 
            neighbor_tuple = tuple(neighbor)
            potential_cost = act_cost[current_state_tuple] + 1 #Potential cost of successor.

            #Checking if neighbor has been visited, is not in the actual cost, or if the potential cost is lower than
            #the previously recorded cost if it is in the actual cost.
            if neighbor_tuple not in visited and (neighbor_tuple not in act_cost or potential_cost < act_cost[neighbor_tuple]):
                act_cost[neighbor_tuple] = potential_cost
                est_cost = get_manhattan_distance(neighbor, goal_state)
                total_cost = potential_cost + est_cost
                heapq.heappush(pq, (total_cost, neighbor, (potential_cost, -1)))
                parent_state[neighbor_tuple] = current_state_tuple
    
    
    
    for state_info in state_info_list:
        current_state = state_info[0]
        h = state_info[1]
        move = state_info[2]
        print(current_state, "h={}".format(h), "moves: {}".format(move))
    print("Max queue length: {}".format(max_length))



if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()
    #
    #print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    #print()

    #solve([4,3,0,5,1,6,7,2,0])
    #print()
