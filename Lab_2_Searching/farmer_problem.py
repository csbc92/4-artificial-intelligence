class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    print("fringe: {}".format(fringe))
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''
def INSERT(node, queue):
    #queue.insert(0, node) # LIFO aka Depth-first search. New elements goes in at start.

    queue.append(node)  # FIFO aka Breadth-first search. New elements goes in at end.

    return queue


'''
Insert list of nodes into the fringe
'''
def INSERT_ALL(list, queue):
    for node in list:
            INSERT(node, queue)
    return queue


'''
Remove first element from fringe
'''
def REMOVE_FIRST(queue):
    if len(queue) != 0:
        return queue.pop(0)


'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


# States: Farmer, Wolf, Goat, Cabbage
# w = west of river
# e = east of river
A_1 = ('w', 'w', 'w', 'w')
B_2 = ('w', 'w', 'w', 'e')
C_3 = ('w', 'w', 'e', 'w')
D_4 = ('w', 'w', 'e', 'e')  # Illegal, Goat eats Cabbage
E_5 = ('w', 'e', 'w', 'w')
F_6 = ('w', 'e', 'w', 'e')
G_7 = ('w', 'e', 'e', 'w')  # Illegal, Wolf eats Goat
H_8 = ('w', 'e', 'e', 'e')  # No sense, to make farmer stand alone on one side, since the problem would have been solved
I_9 = ('e', 'w', 'w', 'w')  # No sense, to make farmer stand alone on one side, since the problem would have been solved
J_10 = ('e', 'w', 'w', 'e')  # Illegal, Wolf eats Goat
K_11 = ('e', 'w', 'e', 'w')
L_12 = ('e', 'w', 'e', 'e')
M_13 = ('e', 'e', 'w', 'w')  # Illegal, Goat eats Cabbage
N_14 = ('e', 'e', 'w', 'e')
O_15 = ('e', 'e', 'e', 'w')
P_16 = ('e', 'e', 'e', 'e')

INITIAL_STATE = A_1
GOAL_STATE = P_16

STATE_SPACE = {A_1: [K_11],
               K_11: [A_1, C_3],
               C_3: [K_11, L_12, O_15],
               L_12: [B_2, C_3],
               B_2: [L_12, N_14],
               N_14: [B_2, E_5, F_6],
               F_6: [N_14, P_16],
               O_15: [C_3, E_5],
               E_5: [N_14, O_15]}

'''
Run tree search and display the nodes in the path to goal node
'''
def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()