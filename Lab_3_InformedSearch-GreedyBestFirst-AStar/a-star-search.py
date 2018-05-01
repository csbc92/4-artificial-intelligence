from urllib.parse import to_bytes

from search_vacuum import heuristic


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
        index_to_remove = GET_LOWEST_TOTAL_COST_NODE(queue)
        return queue.pop(index_to_remove)

def GET_LOWEST_TOTAL_COST_NODE(queue):
    lowest_total_cost_index = -1

    for current_node in queue:
        if lowest_total_cost_index == -1:
            lowest_total_cost_index = queue.index(current_node)
            continue

        current_node_cost = GET_TOTAL_COST(current_node)
        lowest_node_cost = GET_TOTAL_COST(queue[lowest_total_cost_index])
        if current_node_cost < lowest_node_cost:
            lowest_total_cost_index = queue.index(current_node)

    return lowest_total_cost_index

def GET_TOTAL_COST(node):
    heuristic = node.STATE[0][1]
    path_cost = node.STATE[1]
    for parent_node in node.PARENT_NODE.path():
        if len(parent_node.STATE[0]) > 1:  # only add the path_cost if it exists
            path_cost += parent_node.STATE[2]
    total_cost = heuristic + path_cost

    return total_cost

'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]


# STATES with Location and Heuristic cost to GOAL in direct distance (euclidean space)
A = ('A', 6, 0)
B = ('B', 5, 1)
C = ('C', 5, 2)
D = ('D', 2, 4)
E_1 = ('E', 4, 1)
E_2 = ('E', 4, 4)
F = ('F', 5, 5)
G_1 = ('G', 4, 1)
G_2 = ('G', 4, 2)
H_1 = ('H', 1, 3)
H_2 = ('H', 1, 1)
I = ('I', 2, 4)
J = ('J', 1, 2)
K_1 = ('K', 0, 6)
K_2 = ('K', 0, 6)
L_1 = ('L', 0, 5)
L_2 = ('L', 0, 3)


INITIAL_STATE = A
GOAL_STATE = 'L'

# State-space represents the possible paths from one node to another,
# and the cost of traveling the path (expanding the node).
# So data structure is: {Current-node: (Next-node, heuristic, cost), ....}
# basically a map with a tuple: (Next-node, heuristic, cost)
# It is abused that the fact: sometuple + (someitem,) returns a completely new tuple.
"""
STATE_SPACE = {A: [B+(1,), C+(2,), D+(4,)],
               B: [A+(1,), F+(5,), E+(4,)],
               C: [A+(2,), E+(1,)],
               D: [A+(4,), H+(1,), I+(4,), J+(2,)],
               E: [B+(4,), C+(1,), G+(2,), H+(3,)],
               F: [B+(4,), G+(1,)],
               G: [F+(1,), E+(2,), K+(6,)],
               H: [D+(1,), E+(3,), K+(6,), L+(5,)],
               I: [D+(4,), L+(3,)],
               J: [D+(2,)],
               K: [G+(6,), H+(6,)],
               L: [H+(5,), I+(3,)]}
"""
"""
STATE_SPACE = {A: [(B, 1), (C, 2), (D, 4)],
               B: [(A, 1), (F, 5), (E, 4)],
               C: [(A, 2), (E, 1)],
               D: [(A, 4), (H, 1), (I, 4), (J, 2)],
               E: [(B, 4), (C, 1), (G, 2), (H, 3)],
               F: [(B, 4), (G, 1)],
               G: [(F, 1), (E, 2), (K, 6)],
               H: [(D, 1), (E, 3), (K, 6), (L, 5)],
               I: [(D, 4), (L, 3)],
               J: [(D, 2)],
               K: [(G, 6), (H, 6)],
               L: [(H, 5), (I, 3)]}
"""


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
