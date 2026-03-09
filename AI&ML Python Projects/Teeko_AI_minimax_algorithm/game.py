import random
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        # Set to True if you would like to run gradescope against the challenge AI!
        # Leave as False if you would like to run the gradescope tests faster for debugging.
        # You can still get full credit with this set to False
        return True

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        self.depth_limit = 3 #Setting depth limit for time constraint, considering 3 moves in advance. 
        total_pieces = 25 - sum(row.count(' ') for row in state) #25 total spaces minus total empty spaces. 
        drop_phase = total_pieces < 8 #If less than 8 total pieces, we are in the drop phase. 

        successors = self.succ(state, self.my_piece)
        optimal_value = float('-inf') #Initializing as negative infinity. 
        optimal_move = None #Initializing as none. 

        for move, succ_state in successors:
            value = self.min_value(succ_state, 1) #Getting the value from the successor state of a successor. 
            if value > optimal_value: #If this value is better than the current best value, that value is now the best value. 
                optimal_value = value
                optimal_move = move #Move belonging to that successor is now the best move. 

        return optimal_move

    def succ(self, state, piece): #Adding a piece argument to distinguish between my AI player and the opponent. 
        successors = []
        total_pieces = 25 - sum(row.count(' ') for row in state) #Calculating again since succ() can be called with different game states in the minimax recursion. 
        drop_phase = total_pieces < 8 #

        if drop_phase:
            for i in range(5): #Iterating over all spaces on the game board. 
                for j in range(5):
                    if state[i][j] == ' ': #Placing piece in an empty space. 
                        updated_state = [row[:] for row in state]  #Deep copy
                        updated_state[i][j] = piece
                        move = [(i, j)]
                        successors.append((move, updated_state))
        else:
            #Continued gameplay, move one of the player's pieces to an adjacent empty cell.
            positions = [(i, j) for i in range(5) for j in range(5) if state[i][j] == piece] #Find positions of player's pieces.
            for (i, j) in positions: #Iterating over possible movements. 
                for di in [-1, 0, 1]: #Find adjacent cells. 
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue #Skip when no movement. 
                        ni, nj = i + di, j + dj #Calculating new position. 
                        if 0 <= ni < 5 and 0 <= nj < 5 and state[ni][nj] == ' ': #Checking if within boundaries and is empty. 
                            updated_state = [row[:] for row in state] #Deep copy of current state to represent the new state. 
                            updated_state[i][j] = ' ' #Remove from current position. 
                            updated_state[ni][nj] = piece #Place piece at new position. 
                            move = [(ni, nj), (i, j)] #Recording the move as tuple. 
                            successors.append((move, updated_state)) #Adding move and result state to list of successors. 

        return successors

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        #check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j]==self.my_piece else -1
        
        #check / diagonal wins
        for i in range(2):
            for j in range(3,5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j]==self.my_piece else -1
        
        #check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1] == state[i+1][j] == state[i+1][j+1]:
                    return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet


    def count(self, s, i, j, p, di, dj): #Counts consectuive pieces in a given direction for heuristic. Adapted from coding session.

        cur = 1
        n = len(s)
        m = len(s[0])
        for k in range(1, 4): #Forward 
            ni, nj = i + k * di, j + k * dj
            if 0 <= ni < n and 0 <= nj < m and s[ni][nj] == p:
                cur += 1
            else:
                break
        for k in range(1, 4): #Backward
            ni, nj = i - k * di, j - k * dj
            if 0 <= ni < n and 0 <= nj < m and s[ni][nj] == p:
                cur += 1
            else:
                break
        return cur


    def get_h(self, s, p): #Calculating heuristic value for player p. Also adapted from coding session. 
        h = 0
        n = len(s)
        m = len(s[0])
        for i in range(n):
            for j in range(m):
                if s[i][j] == p:
                    for d in [[1, 0], [0, 1], [1, 1], [1, -1]]:
                        cur = self.count(s, i, j, p, d[0], d[1])
                        h = max(h, cur)
        return h / 4.0  #Dividing by 4 since the maximum sequence is 4.


    def check_box(self, s, p): #Additional heuristic checking for the maxiumum number of player's pieces in a 2x2 box (one of the winning conditions). 
        h = 0
        n = len(s)
        m = len(s[0])
        for i in range(n-1):
            for j in range(m-1):
                count_pieces = sum([
                    s[i][j] == p,
                    s[i][j+1] == p,
                    s[i+1][j] == p,
                    s[i+1][j+1] == p
                ])
                h = max(h, count_pieces)
        return h / 4.0  # Maximum in a box is 4 pieces. 

    def heuristic_game_value(self, state): #Evaluating non-terminal states. 
        #Checking if the state is terminal.
        value = self.game_value(state)
        if value != 0:
            return value

        mapping = {self.my_piece: 1, self.opp: -1, ' ': 0} #Mapping the board to numeric values. 
        s = [[mapping[cell] for cell in row] for row in state]

        my_ai_score = self.get_h(s, 1) + self.check_box(s, 1) #Calculating scores with get_h and check_box heuristic. 
        opp_score = self.get_h(s, -1) + self.check_box(s, -1)

        # Calculate heuristic value
        return (my_ai_score - opp_score) / 2  #Normalizing between -1 and 1.


    def max_value(self, state, depth): #Max player/my AI.
        value = self.game_value(state) #Check if terminal state/game is over. 
        if value != 0:
            return value
        if depth >= self.depth_limit: #Check if depth limit has been met. 
            return self.heuristic_game_value(state) #Return the heuristic value for non-terminal states. 
        v = float('-inf')
        for move, successor_state in self.succ(state, self.my_piece): #Generate all possible successor states for max player. 
            v = max(v, self.min_value(successor_state, depth + 1)) #Recursively calling min_value to evaluate response of opponent. 
        return v


    def min_value(self, state, depth): #Min player/opponent, same strategy as above. 
        value = self.game_value(state)
        if value != 0:
            return value
        if depth >= self.depth_limit:
            return self.heuristic_game_value(state)
        v = float('inf')
        for move, successor_state in self.succ(state, self.opp): #Generate all possible successor states for min player.
            v = min(v, self.max_value(successor_state, depth + 1))
        return v


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
