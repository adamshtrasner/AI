from board import Board
from search import SearchProblem, ucs
import util

COST_FOR_ILLEGAL_STATE = 999999

class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


class BlokusCornersProblem(SearchProblem):

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.corners = [(0, 0),
                        (board_h - 1, 0),
                        (0, board_w - 1),
                        (board_w - 1, board_h - 1)]
        self.starting_point = starting_point

    def get_start_state(self) -> Board:
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state: Board) -> bool:
        return are_targets_covered(state, self.corners)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return cost_by_number_of_tiles(actions)


def blokus_corners_heuristic(state: Board, problem: BlokusCornersProblem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """

    # The heuristic: returns the minimum number of tiles of
    # a possible piece in the current state, for some corner
    # that is still free.

    min_number_of_tiles = max(state.board_h, state.board_w)
    for i in range(state.piece_list.get_num_pieces()):
        if state.pieces[0][i]:
            min_number_of_tiles = min(min_number_of_tiles, state.piece_list.get_piece(i).get_num_tiles())

    for corner in problem.corners:
        if state.get_position(corner[1], corner[0]):
            if state.check_tile_legal(0, corner[1], corner[0]) and state.connected[0, corner[1], corner[0]]:
                if min_number_of_tiles < min(state.board_h, state.board_w):
                    return min_number_of_tiles
                return 0
            return COST_FOR_ILLEGAL_STATE

    # If out of loop that means we covered all corners
    return 0


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state: Board) -> bool:
        return are_targets_covered(state, self.targets)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return cost_by_number_of_tiles(actions)


def blokus_cover_heuristic(state, problem):
    # TODO: CHECK if this is really ADMISSIBLE and CONSISTENT !!!
    for corner in problem.targets:
        if not state.check_tile_legal(0, corner[1], corner[0]):
            if state.get_position(corner[1], corner[0]):
                return COST_FOR_ILLEGAL_STATE
    return chebyshev_heuristic(state, problem)


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


# ------------ Helper classes/functions ------------


def cost_by_number_of_tiles(actions):
    cost = 0
    for action in actions:
        cost += action.piece.get_num_tiles()
    return cost


def are_targets_covered(state, targets):
    for target in targets:
        if state.get_position(target[1], target[0]):
            return False
    return True


def chebyshev_heuristic(state, problem):
    # If the state is the starting state, the list of points would
    # have the starting point only
    legal_points = list()
    if state == problem.get_start_state():
        legal_points.append(problem.starting_point)
    else:
        # Go over all points that can be reached legally
        for i in range(state.board_h):
            for j in range(state.board_w):
                if state.check_tile_legal(0, j, i) and state.connected[0, j, i]:
                    legal_points.append((i, j))

    # return inf if the list of those points is empty
    if not legal_points:
        return COST_FOR_ILLEGAL_STATE

    # compute chebyshev's distance for each of the legal points to
    # each corner, save the minimum of each distance (save the cost of
    # the closest point to a particular corner according to chebyshev's distance)
    # and apply max for each corner
    max_distance = 0
    for target in problem.targets:
        if state.get_position(target[1], target[0]):
            max_distance = max(max_distance,
                               min(chebyshev_distance(point, target) for point in legal_points))
    return max_distance


def chebyshev_distance(xy1, xy2):
    return max(abs(xy1[0] - xy2[0]), abs(xy1[1] - xy2[1]))


# --------------------------------------------------
