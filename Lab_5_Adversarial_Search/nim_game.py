from math import floor


def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    state = argmax(successors_of(state), lambda s: min_value(s))
    return state


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    for pile in state:
        if pile > 2: # RULE IN GAME: Only piles that are greater than 2 can be split
            return False

    # If no piles can be split, we are done
    return True


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    # Decides which player's turn it is
    if len(state) % 2 == 1:
        player = 'MIN'  # X makes odd numbered moves
    else:
        player = 'MAX'

    if not is_terminal(state):
        return 0

    if player == 'MAX':
        return 1
    elif player == 'MIN':
        return -1




def has_won(state, player):
    """
    Returns 1 if the player has won, otherwise -1
    """

def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    successors = []

    # Creates a successor for each available move
    for pile in state:
        if pile > 2: # Check if the pile can be split
            max_elements_to_remove = floor(pile/2) # Max elements that can be removed in the pile

            for i in range(1, max_elements_to_remove+1):
                if pile/2 != i: # RULE IN GAME: Not allowed to split pile in half
                    successor = state[:]  # Copy list
                    successor.remove(pile)  # Remove old pile
                    successor.insert(0, pile-i)  # Insert the 1st split pile
                    successor.insert(0, i)  # Insert the 2nd split pile
                    successors.append(successor)

    # print('Successor: ' + str(successors))
    return successors


def display(state):
    print("-----")
    print(state)


def main():
    piles = [50]
    while not is_terminal(piles):
        piles = minmax_decision(piles)
        if not is_terminal(piles):
            display(piles)
            print("Your move: ")
            piles = [int(x) for x in input().split()]
    display(piles)
    print(utility_of(piles))


def argmax(iterable, func):
    return_val = max(iterable, key=func)
    return return_val


"""
This program searches through all possible states down to the end of the game tree.
After the search has been done, the agent knows which moves are the best, depending on the opponent's moves.
The algorithm is a minimax algorithm.
"""
if __name__ == '__main__':
    main()
