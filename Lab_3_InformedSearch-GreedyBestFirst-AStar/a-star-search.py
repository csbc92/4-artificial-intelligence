from urllib.parse import to_bytes

from search_vacuum import heuristic


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.PATH_COST = 0  # Initial path cost. Represents the path cost from initial node -> to get to this node


    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def calculate_path_cost(self):
        # Calculate the new path cost of this node by the formula:
        # path-cost = parent-path-cost + path-cost
        if self.PARENT_NODE is not None and len(self.PARENT_NODE.STATE) > 2:
            self.PATH_COST += self.PARENT_NODE.STATE[2]
        if len(self.STATE) > 2:  # A state has the format (<name>, <heuristic>, <path-cost>) where path-cost may be missing.
            self.PATH_COST += self.STATE[2]

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    explored_nodes = set()
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    print("fringe: {}".format(fringe))
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        explored_nodes.add(node)
        if node.STATE[0] == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe, explored_nodes)
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
        s.calculate_path_cost()
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
def INSERT_ALL(list, queue, explored_nodes):
    for node in list:
        if node not in explored_nodes:
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
    heuristic = node.STATE[1]  # Get the heuristic
    path_cost = node.PATH_COST

    total_cost = heuristic + path_cost

    return total_cost

'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    state_list = list(state)  # Prepare the tuple for mutation

    if len(state_list) > 2:
        state_list.pop(len(state_list)-1)  # Remove the last element (path cost) from the state
        state = tuple(state_list)  # Make the list into a tuple again

    return STATE_SPACE[state]


# STATES with Location and Heuristic cost to GOAL in direct distance (euclidean space)
A = ('A', 6)
B = ('B', 5)
C = ('C', 5)
D = ('D', 2)
E = ('E', 4)
F = ('F', 5)
G = ('G', 4)
H = ('H', 1)
I = ('I', 2)
J = ('J', 1)
K = ('K', 0)
L = ('L', 0)


INITIAL_STATE = A
GOAL_STATE = 'K'

# State-space represents the possible paths from one node to another,
# and the cost of traveling the path (expanding the node).
# It is abused that, in python you can mutate tuples like: sometuple + (someitem,) returns a completely new tuple.


# Experimental - a directional graph, that is you can only navigate "down" in the graph, not up again.
STATE_SPACE = {A: [B+(1,), C+(2,), D+(4,)],
               B: [F+(5,), E+(4,)],
               C: [E+(1,)],
               D: [H+(1,), I+(4,), J+(2,)],
               E: [G+(2,), H+(3,)],
               F: [G+(1,)],
               G: [K+(6,)],
               H: [K+(6,), L+(5,)],
               I: [L+(3,)],
               J: [],
               K: [],
               L: []}
"""
# Experimental - A bidirectional graph
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
