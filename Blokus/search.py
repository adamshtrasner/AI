"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    return generic_search(problem, util.Stack())


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return generic_search(problem, util.Queue())


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    cost_func = lambda state: problem.get_cost_of_actions(state.list_of_actions)
    return generic_search(problem, util.PriorityQueueWithFunction(cost_func))


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # according to: f(v) = h(v) + g(v)
    # where h is the heuristic and g is the cost to v so far
    cost_func = lambda state: \
        heuristic(state.state, problem) + problem.get_cost_of_actions(state.list_of_actions)
    return generic_search(problem, util.PriorityQueueWithFunction(cost_func))


# Abbreviations

bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search


# ------------ Helper classes/functions ------------


def generic_search(problem, fringe):
    """
    A generic search function.
    This function uses the algorithm for graph search taught in class.
    The data structure of the fringe is dependent on the search we choose,
    and every element in the fringe is of class State.
    """
    closed = set()
    path_of_actions = list()
    fringe.push(State(problem.get_start_state(), path_of_actions))

    while not fringe.isEmpty():
        curr = fringe.pop()

        if problem.is_goal_state(curr.state):
            return curr.list_of_actions

        if curr.state not in closed:
            closed.add(curr.state)
            successors = problem.get_successors(curr.state)
            for successor in successors:
                # Append state with current successor and list of actions
                # with the added successor's action
                fringe.push(State(successor[0], curr.list_of_actions + [successor[1]]))

# We created a class because adding tuples or lists of size 2 into the fringe
# raised an error because the push function fails (__lt__ exists for both tuples
# and lists)


class State:
    """
    A class of state which represents an item in the fringe,
    in order to keep the path of actions for each state in the fringe.
    """
    def __init__(self, state, list_of_actions):
        self.state = state
        self.list_of_actions = list_of_actions
# --------------------------------------------------
