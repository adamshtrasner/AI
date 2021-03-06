import numpy as np
import abc
import util
from game import Agent, Action
import math


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        "*** YOUR CODE HERE ***"

        # Taking max score out of the scores of the successors of the current game state's successor.
        legal_actions = successor_game_state.get_agent_legal_actions()
        if legal_actions:
            successors_of_successors_scores = [successor_game_state.generate_successor(action=a).score
                                               for a in legal_actions]
            return max(successors_of_successors_scores)
        return 0


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        legal_actions = game_state.get_legal_actions(0)
        actions = list()

        for action in legal_actions:
            successor = game_state.generate_successor(0, action)
            actions.append((self.minmax_algorithm(successor, self.depth, 1), action))

        return max(actions, key=lambda t: t[0])[1]

    def minmax_algorithm(self, game_state, depth, player_index):
        legal_actions = game_state.get_legal_actions(player_index)
        is_terminal_node = game_state.done

        if depth == 0 or is_terminal_node:
            return self.evaluation_function(game_state)

        successors = [game_state.generate_successor(player_index, action) for action in legal_actions]

        if player_index == 0:
            return max(self.minmax_algorithm(s, depth, 1) for s in successors)
        else:
            return min(self.minmax_algorithm(s, depth - 1, 0) for s in successors)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legal_actions = game_state.get_legal_actions(0)

        actions = list()
        for action in legal_actions:
            successor = game_state.generate_successor(0, action)
            actions.append((self.alpha_beta_pruning(successor, self.depth, -math.inf, math.inf, 1), action))

        return max(actions, key=lambda t: t[0])[1]

    def alpha_beta_pruning(self, game_state, depth, alpha, beta, player_index):
        legal_actions = game_state.get_legal_actions(player_index)
        is_terminal_node = game_state.done

        if depth == 0 or is_terminal_node:
            return self.evaluation_function(game_state)

        successors = [game_state.generate_successor(player_index, action) for action in legal_actions]

        if player_index == 0:
            for s in successors:
                alpha = max(alpha, self.alpha_beta_pruning(s, depth, alpha, beta, 1))
                if beta <= alpha:
                    break
            return alpha
        else:
            for s in successors:
                beta = min(beta, self.alpha_beta_pruning(s, depth - 1, alpha, beta, 0))
                if beta <= alpha:
                    break
            return beta


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legal_actions = game_state.get_legal_actions(0)

        actions = list()
        for action in legal_actions:
            successor = game_state.generate_successor(0, action)
            actions.append((self.expectimax_algorithm(successor, self.depth, 1), action))
        return max(actions, key=lambda t: t[0])[1]

    def expectimax_algorithm(self, game_state, depth, player_index):
        legal_actions = game_state.get_legal_actions(player_index)
        is_terminal_node = game_state.done

        if depth == 0 or is_terminal_node:
            return self.evaluation_function(game_state)

        successors = [game_state.generate_successor(player_index, action) for action in legal_actions]
        n = len(successors)

        if player_index == 0:
            return max(self.expectimax_algorithm(s, depth, 1) for s in successors)
        else:
            return (1 / n) * sum([self.expectimax_algorithm(s, depth - 1, 0) for s in successors])


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: We used a sum of 2 evaluation functions minus penalties:
                 (1) number of empty tiles - The more empty tiles you have the more you're far away from losing.
                 Therefore, we scored each state with this number - squared.
                 (2) weighted sum of board - We used a score matrix, giving each place in the board
                 a score according to the board's monotonicity: We found out after much research and
                 game plays that keeping higher tiles more clustered to the corner will result in a
                 better score, and so we used a snake shaped like matrix, giving higher scores as u get close
                 to the top left corner, and also it's reasonable to put tiles with different values in a
                 monotonic order so that they could merge consecutively, and so the reasoning behind the snake
                 shaped score matrix.
    """
    board = current_game_state.board
    empty_tiles = num_of_empty_tiles(current_game_state)

    return empty_tiles ** 2 + weighted_sum_of_board(board)


# Abbreviation
better = better_evaluation_function


# ------------ Helper functions ------------


def num_of_empty_tiles(game_state):
    """
    Number of empty tiles heuristic
    """
    return len(game_state.get_empty_tiles()[0])


SNAKE_MATRIX = np.array([[6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1], [3, 2, 1, 0]]) ** 2


def weighted_sum_of_board(board):
    return np.sum(SNAKE_MATRIX * board)
# --------------------------------------------------
