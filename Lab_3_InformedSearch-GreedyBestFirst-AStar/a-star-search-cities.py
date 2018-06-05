from urllib.parse import to_bytes

from search_vacuum import heuristic


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.PATH_COST = 0  # Initial path cost. Represents the path cost from initial node -> to get to this node
        self.TOTAL_PATH_COST = 0 # Initial total path cost. Represents the path cost + heuristic


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

        parent = self.PARENT_NODE
        while parent is not None:
            if parent is not None and len(parent.STATE) > 2:
                self.PATH_COST += int(parent.STATE[2])

            parent = parent.PARENT_NODE

        if len(self.STATE) > 2:  # A state has the format (<name>, <heuristic>, <path-cost>) where path-cost may be missing.
            self.PATH_COST += self.STATE[2]

        self.TOTAL_PATH_COST = self.PATH_COST + self.STATE[1]  # f(x) = g(x) + h(x)



        #if self.PARENT_NODE is not None and len(self.PARENT_NODE.STATE) > 2:
        #    self.PATH_COST += self.PARENT_NODE.STATE[2]
        #if len(self.STATE) > 2:  # A state has the format (<name>, <heuristic>, <path-cost>) where path-cost may be missing.
        #    self.PATH_COST += self.STATE[2]

        #self.TOTAL_PATH_COST = self.PATH_COST + self.STATE[1]  # f(x) = g(x) + h(x)

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Total path cost: ###' + str(self.TOTAL_PATH_COST) + '### - Depth: ' + str(self.DEPTH)


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
        explored_nodes.add(node.STATE[0])
        if node.STATE[0] == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe, explored_nodes)
        print("explored nodes: {}".format(explored_nodes))
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
        if node.STATE[0] in explored_nodes:
            continue
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

        current_node_cost = current_node.TOTAL_PATH_COST #GET_TOTAL_COST(current_node)
        lowest_node_cost = queue[lowest_total_cost_index].TOTAL_PATH_COST #GET_TOTAL_COST(queue[lowest_total_cost_index])
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
ARAD = ('ARAD', 366)
ZERIN = ('ZERIND', 374)
ORADEA = ('ORADEA', 380)
TIMIASORA = ('TIMIASORA', 329)
LUGOJ = ('LUGOJ', 244)
MEHADIA = ('MEHADIA', 241)
DOBRETA = ('DOBRETA', 242)
SIBIU = ('SIBIU', 253)
RIMNICU_VILCEA = ('RIMNICU_VILCEA', 193)
CRAIOVA = ('CRAIOVA', 160)
FAGARAS = ('FAGARAS', 176)
PITESTI = ('PITESTI', 10)

BUCHAREST = ('BUCHAREST', 0)
GIURGIU = ('GIURGIU', 77)
URZICENI = ('URZICENI', 80)
HIRSOVA = ('HIRSOVA', 151)
EFORIE = ('EFORIE', 161)
VASLUI = ('VASLUI', 199)
IASI = ('IASI', 226)
NEAMT = ('NEAMT', 234)


INITIAL_STATE = ARAD
GOAL_STATE = 'BUCHAREST'

# State-space represents the possible paths from one node to another,
# and the cost of traveling the path (expanding the node).
# It is abused that, in python you can mutate tuples like: sometuple + (someitem,) returns a completely new tuple.

# Experimental - A bidirectional graph from the book
STATE_SPACE = {ARAD: [ZERIN+(75,), SIBIU+(140,), TIMIASORA+(118,)],
               ZERIN: [ARAD+(75,), ORADEA+(71,)],
               ORADEA: [ZERIN+(71,), SIBIU+(151,)],
               TIMIASORA: [ARAD+(118,), LUGOJ+(111,)],
               LUGOJ: [TIMIASORA+(111,), MEHADIA+(70,)],
               MEHADIA: [LUGOJ+(70,), DOBRETA+(75,)],
               SIBIU: [ORADEA+(151,), ARAD+(140,), FAGARAS+(99,), RIMNICU_VILCEA+(80,)],
               RIMNICU_VILCEA: [SIBIU+(80,), CRAIOVA+(146,), PITESTI+(97,)],
               CRAIOVA: [DOBRETA+(120,), RIMNICU_VILCEA+(146,), PITESTI+(138,)],
               DOBRETA: [MEHADIA+(75,), CRAIOVA+(120,)],
               FAGARAS: [SIBIU+(99,), BUCHAREST+(211,)],
               PITESTI: [RIMNICU_VILCEA+(97,), CRAIOVA+(138,), BUCHAREST+(101,)],
               BUCHAREST: [FAGARAS+(211,), PITESTI+(101,), URZICENI+(85,), GIURGIU+(90,)],
               GIURGIU: [BUCHAREST+(90,)],
               URZICENI: [BUCHAREST + (85,), VASLUI+(142,), HIRSOVA+(98,)],
               HIRSOVA: [URZICENI + (98,), EFORIE + (86,)],
               EFORIE: [HIRSOVA + (86,)],
               VASLUI: [URZICENI + (142,), IASI + (92,)],
               IASI: [VASLUI + (92,), NEAMT + (87,)],
               NEAMT: [IASI + (87,)]}

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
