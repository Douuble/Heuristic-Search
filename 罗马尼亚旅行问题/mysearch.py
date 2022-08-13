import sys
from collections import deque


class Problem:  # 抽象类，在子类中实现函数
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return list(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    # def value(self, state):
    #     """For optimization problems, each state has a value. Hill Climbing
    #     and related algorithms try to maximize this value."""
    #     raise NotImplementedError


    def h(self, node):
        # 用于计算启发式
        raise NotImplementedError


# ______________________________________________________________________________
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


#############################


neighbor_map = {'Arad': ['Zerind', 'Sibiu', 'Timisoara'], 'Timisoara': ['Arad', 'Lugoj'],
                'Lugoj': ['Timisoara', 'Mehadia'], 'Mehadia': ['Lugoj', 'Drobeta'],
                'Drobeta': ['Mehadia', 'Craiova'], 'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
                'Rimnicu Vilcea': ['Sibiu', 'Pitesti'],
                'Sibiu': ['Oradea', 'Arad', 'Rimnicu Vilcea', 'Fagaras'], 'Oradea': ['Zerind', 'Sibiu'],
                'Zerind': ['Arad', 'Oradea'], 'Fagaras': ['Sibiu', 'Bucharest'],
                'Pitesti': ['Rimnicu Vilcea', 'Craiova', 'Bucharest'],
                'Bucharest': ['Urziceni', 'Pitesti', 'Giurgiu', 'Fagaras']
                }

neighbormapWithweight = {'Arad': {'Zrind': 75, 'Sibiu': 140, 'Timisoara': 118},
                         'Timisoara': {'Arad': 118, 'Lugoj': 111},
                         'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
                         'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
                         'Drobeta': {'Mehadia': 75, 'Craiova': 120},
                         'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},
                         'Rimnicu Vilcea': {'Sibiu': 80, 'Pitesti': 97},
                         'Sibiu': {'Oradea': 151, 'Arad': 140, 'Rimnicu Vilcea': 80, 'Fagaras': 99},
                         'Oradea': {'Zerind': 71, 'Sibiu': 151},
                         'Zerind': {'Arad': 75, 'Oradea': 71},
                         'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
                         'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
                         'Bucharest': {'Urziceni': 85, 'Pitesti': 101, 'Giurgiu': 90, 'Fagaras': 211}
                         }

# romania_map.locations = dict(
#     Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
#     Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
#     Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
#     Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
#     Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
#     Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
#     Vaslui=(509, 444), Zerind=(108, 531)

# 到Bucharest的直线距离，启发式
HSLD = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160,
    'Drobeta': 242, 'Eforie': 161, 'Fagaras': 176,
    'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226,
    'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
    'Vaslui': 199, 'Zerind': 374
}


class Romania(Problem):

    def __init__(self, initial, goal=None):
        self.initial = 'Arad'
        self.goal = 'Bucharest'


    def actions(self, state):
        list_op = neighbor_map.get(state, '')
        return list_op

    def result(self, state, action):
        return action

    def h(self, node):
        return HSLD[node.state]


def greedy_best_first_graph_search(problem, h=None):
    frontier = []
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier.append(node)
    explored = set()  # 去除重复元素的集合
    while frontier:  # frontier判空
        node = frontier.pop()
        if problem.goal_test(node):
            return node
        explored.add(node)  # 放入已扩展节点
        for child in node.expand(problem):
            if child not in explored and child not in frontier:  # 如果子节点没有被扩展过，则加入frontier表中
                frontier.append(child)
                frontier.sort(key=lambda n: problem.h(n), reverse=True)
    return node

def astar_search(problem, h=None):
    frontier = []
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier.append(node)
    explored = set()  # 去除重复元素的集合
    while frontier:  # frontier判空
        node = frontier.pop()
        if problem.goal_test(node):
            return node
        explored.add(node)  # 放入已扩展节点
        for child in node.expand(problem):
            if child not in explored and child not in frontier:  # 如果子节点没有被扩展过，则加入frontier表中
                frontier.append(child)
                frontier.sort(key=lambda n: problem.h(n)+n.path_cost, reverse=True)  #不明白参数该怎么传
    return node


r = Romania('Arad', 'Bucharest')
result1 = greedy_best_first_graph_search(r)
print(result1.path())
result2=astar_search(r)
print(result1.path())



#
# ################################################
# class EightPuzzle(Problem):
#     """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
#     squares is a blank. A state is represented as a tuple of length 9, where  element at
#     index i represents the tile number  at index i (0 if it's an empty square) """
#
#     def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
#         """ Define goal state and initialize a problem """
#         super().__init__(initial, goal)
#
#     def find_blank_square(self, state):
#         """Return the index of the blank square in a given state"""
#         return state.index(0)
#
#     def actions(self, state):
#         """ Return the actions that can be executed in the given state.
#         The result would be a list, since there are only four possible actions
#         in any given state of the environment """
#
#         possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#         index_blank_square = self.find_blank_square(state)
#
#         if index_blank_square % 3 == 0:
#             possible_actions.remove('LEFT')
#         if index_blank_square < 3:
#             possible_actions.remove('UP')
#         if index_blank_square % 3 == 2:
#             possible_actions.remove('RIGHT')
#         if index_blank_square > 5:
#             possible_actions.remove('DOWN')
#
#         return possible_actions
#
#     def result(self, state, action):
#         """ Given state and action, return a new state that is the result of the action.
#         Action is assumed to be a valid action in the state """
#
#         # blank is the index of the blank square
#         blank = self.find_blank_square(state)
#         new_state = list(state)
#
#         delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
#         neighbor = blank + delta[action]
#         new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
#
#         return tuple(new_state)
#
#     def goal_test(self, state):
#         """ Given a state, return True if state is a goal state or False, otherwise """
#
#         return state == self.goal
#
#     def check_solvability(self, state):
#         """ Checks if the given state is solvable """
#
#         inversion = 0
#         for i in range(len(state)):
#             for j in range(i + 1, len(state)):
#                 if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
#                     inversion += 1
#
#         return inversion % 2 == 0
#
#     def h(self, node):
#         """ Return the heuristic value for a given state. Default heuristic function used is
#         h(n) = number of misplaced tiles """
#         h=0
#         for i in range(0,9):
#            if self.state[i]!=self.goal[i]:
#                h=h+1
#         ''' please implement your heuristic function'''
#         return h
#
#     def astar_search(problem, h=None):
#         frontier = []
#         node = Node(problem.initial)
#         if problem.goal_test(node.state):
#             return node
#         frontier.append(node)
#         explored = set()  # 去除重复元素的集合
#         while frontier:  # frontier判空
#             node = frontier.pop()
#             if problem.goal_test(node):
#                 return node
#             explored.add(node)  # 放入已扩展节点
#             for child in node.expand(problem):
#                 if child not in explored and child not in frontier:  # 如果子节点没有被扩展过，则加入frontier表中
#                     frontier.append(child)
#                     frontier.sort(key=lambda n: problem.h(n), reverse=True)  # 不明白参数该怎么传
#         return node
#
# initial=(2,4,3,1,5,6,7,8,0)
# e=EightPuzzle(initial)
# if e.check_solvability(initial):
#     list1=astar_search(e)

