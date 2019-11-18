# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodDist = 999999
        for food in newFood.asList():
            foodDist = min(manhattanDistance(food, newPos) + 1, foodDist)

        ghostDist = manhattanDistance(newGhostStates[0].getPosition(), newPos) + 1

        if action == 'Stop':
            return -999999

        if not newScaredTimes[0] == 0:
            return successorGameState.getScore() + 1 / foodDist + 10 / ghostDist

        return successorGameState.getScore() + 10 / foodDist + 0.1 * ghostDist

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, index, depth):
            if depth == 0 or gameState.getLegalActions(index % gameState.getNumAgents()) == []:
                return self.evaluationFunction(gameState)
            elif index == gameState.getNumAgents():
                return max_value(gameState, index, depth)
            else:
                return min_value(gameState, index, depth)

        def max_value(gameState, index, depth):
            v = -999999
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                v = max(v, value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index+1, depth-1))
            return v

        def min_value(gameState, index, depth):
            v = 999999
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                v = min(v, value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index+1, depth-1))
            return v

        values = []
        for action in gameState.getLegalActions(self.index):
            values.append((value(gameState.generateSuccessor(self.index, action), self.index+1, self.depth*gameState.getNumAgents()-1), action))
        bestAction = max(values)

        return bestAction[1]

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def value(gameState, index, depth, a, b):
            if depth == 0 or gameState.getLegalActions(index % gameState.getNumAgents()) == []:
                return self.evaluationFunction(gameState)
            elif index == gameState.getNumAgents():
                return max_value(gameState, index, depth, a, b)
            else:
                return min_value(gameState, index, depth, a, b)

        def max_value(gameState, index, depth, a, b):
            v = -999999
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                v = max(v, value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index + 1,
                                 depth - 1, a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def min_value(gameState, index, depth, a, b):
            v = 999999
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                v = min(v, value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index + 1,
                                 depth - 1, a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        values = []
        a = -999999
        b = 999999
        for action in gameState.getLegalActions(self.index):
            values.append((value(gameState.generateSuccessor(self.index, action), self.index + 1,
                                 self.depth * gameState.getNumAgents() - 1, a, b), action))
            a = max(a, value(gameState.generateSuccessor(self.index, action), self.index + 1,
                             self.depth * gameState.getNumAgents() - 1, a, b))
        bestAction = max(values)

        return bestAction[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, index, depth):
            if depth == 0 or gameState.getLegalActions(index % gameState.getNumAgents()) == []:
                return self.evaluationFunction(gameState)
            elif index == gameState.getNumAgents():
                return max_value(gameState, index, depth)
            else:
                return exp_value(gameState, index, depth)

        def max_value(gameState, index, depth):
            v = -999999
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                v = max(v, value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index+1, depth-1))
            return v

        def exp_value(gameState, index, depth):
            v = 0
            for successor in gameState.getLegalActions(index % gameState.getNumAgents()):
                p = 1.0 / len(gameState.getLegalActions(index % gameState.getNumAgents()))
                v += p * value(gameState.generateSuccessor(index % gameState.getNumAgents(), successor), index+1, depth-1)
            return v

        values = []
        for action in gameState.getLegalActions(self.index):
            values.append((value(gameState.generateSuccessor(self.index, action), self.index+1, self.depth*gameState.getNumAgents()-1), action))
        bestAction = max(values)

        return bestAction[1]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodDist = 9999
    for food in newFood.asList():
        foodDist = min(manhattanDistance(food, newPos) + 1, foodDist)

    ghostDist = manhattanDistance(newGhostStates[0].getPosition(), newPos) + 1

    if not newScaredTimes[0] == 0:
        return currentGameState.getScore() + 1 / foodDist + 10 / ghostDist

    return currentGameState.getScore() + 10 / foodDist + 0.1 * ghostDist

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

