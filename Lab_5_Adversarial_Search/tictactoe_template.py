def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    # Return true or false if there is a winner from the utility_of(state)
    if utility_of(state) == 1:
        return True

    if utility_of(state) == -1:
        return True

    # Check if the board is full, i.e. there is no numbers left on the board
    for x in state:
        if isinstance(x, int):
            return False

    if utility_of(state) == 0:
        return True


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    player_x = has_won(state, 'X')
    player_o = has_won(state, 'O')

    # Tie
    if player_x == 1 and player_o == 1:
        return 0

    if player_x == 1:
        return 1

    if player_o == 1:
        return -1

    # No winner if both is -1
    return 0


def has_won(state, player):
    row_1 = state[0:3]
    row_2 = state[3:6]
    row_3 = state[6:9]

    # 1st row
    if row_1[0] == player and row_1[1] == player and row_1[2] == player:
        return 1

    # 2nd row
    if row_2[0] == player and row_2[1] == player and row_2[2] == player:
        return 1

    # 3rd row
    if row_3[0] == player and row_3[1] == player and row_3[2] == player:
        return 1

    # 1st column
    if row_1[0] == player and row_2[0] == player and row_3[0] == player:
        return 1

    # 2nd column
    if row_1[1] == player and row_2[1] == player and row_3[1] == player:
        return 1

    # 3rd column
    if row_1[2] == player and row_2[2] == player and row_3[2] == player:
        return 1

    # diagonal from top left
    if row_1[0] == player and row_2[1] == player and row_3[2] == player:
        return 1

    # diagonal from top right
    if row_1[2] == player and row_2[1] == player and row_3[0] == player:
        return 1

    return -1


def has_won2(state, player):
    n = int(len(state)**0.5) # number of fields in a row, column, diagonal

    uniq_value = 0 # The value represents a unique integer, that indicates if there is a match in row, column or diagonal

    for i in range(0, len(state)):
        if state[i] == player: # Increase the unique value if the player is in that field
            uniq_value += 2**i

    # Check rows
    uniq_row_value = 0
    for j in range(0, len(state)):
        uniq_row_value += 2 ** j

        if (j+1) % n == 0 and j > 0:
            if uniq_value == uniq_row_value:
                return 1  # Player won
            uniq_row_value = 0

    # Check columns
    uniq_col_values = list()
    for i in range(0, n):
        uniq_col_value = 0
        for j in range(0, len(state), n):
            uniq_col_value += 2**(i+j)
        uniq_col_values.append(uniq_col_value)

    if any([x == uniq_value for x in uniq_col_values]):
        return 1  # Player won

    # Check diagonal 1
    uniq_diag_value = 0
    for i in range(0, len(state), n+1):
        uniq_diag_value += 2**i
    if uniq_value == uniq_diag_value:
        return 1  # Player won

    # Check diagonal 2
    uniq_diag_value = 0
    for i in range(n-1, len(state), n - 1):
        uniq_diag_value += 2 ** i
    if uniq_value == uniq_diag_value:
        return 1  # Player won

    return -1  # Player did not win

def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    successors = []
    open = 0
    # How many open spots there are
    for move in range(9):
        if state[move] == move:
            open += 1
    # Decides which player's turn it is
    if open % 2 == 1:
        player = 'X'  # X makes odd numbered moves
    else:
        player = 'O'
    # Creates a successor for each available move
    for move in range(9):
        if state[move] == move:  # Its a 0, 1, 2, etc.
            successor = state[:]  # Copy list
            successor[move] = player  # Place the player
            successors.append((move, successor))
    # print('Successor: ' + str(successors))
    return successors


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


"""
 A method for testing if the winner can be determined properly by the utility function
"""
def test_winner():
    # 1st row
    winner = utility_of(['X', 'X', 'X', 3, 4, 5, 6, 7, 8])
    print(winner == 1)

    # 2nd row
    winner = utility_of([0, 1, 2, 'X', 'X', 'X', 6, 7, 8])
    print(winner == 1)

    # 3rd row
    winner = utility_of([0, 1, 2, 3, 4, 5, 'X', 'X', 'X'])
    print(winner == 1)

    # 1st column
    winner = utility_of(['X', 1, 2, 'X', 4, 5, 'X', 7, 8])
    print(winner == 1)

    # 2nd column
    winner = utility_of([0, 'X', 2, 3, 'X', 5, 6, 'X', 8])
    print(winner == 1)

    # 3rd column
    winner = utility_of([0, 1, 'X', 3, 4, 'X', 6, 7, 'X'])
    print(winner == 1)

    # 1st diagonal, starting upper right corner
    winner = utility_of([0, 1, 'X', 3, 'X', 5, 'X', 7, 8])
    print(winner == 1)

    # 2nd diagonal, starting upper left corner
    winner = utility_of(['X', 1, 2, 3, 'X', 5, 6, 7, 'X'])
    print(winner == 1)

    # Sample game also with player O involved
    winner = utility_of(['X', 'X', 'O', 'X', 'X', 'O', 6, 7, 'O'])
    print(winner == 1)


"""
This program searches through all possible states down to the end of the game tree.
After the search has been done, the agent knows which moves are the best, depending on the opponent's moves.
The algorithm is a minimax algorithm.
"""
if __name__ == '__main__':
    #print("Running test first..")
   #test_winner()
    main()
