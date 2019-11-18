# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    pacStack = util.Stack()
    visited = []
    currentState = problem.getStartState()
    pacStack.push((currentState, ()))

    while not pacStack.isEmpty():
        currentState = pacStack.pop()
        if currentState[0] not in visited:
            visited.append(currentState[0])
            if problem.isGoalState(currentState[0]):
                break
            for successor in problem.getSuccessors(currentState[0]):
                success = True
                for already in visited:
                    if successor[0] == already:
                        success = False
                        break
                if success:
                    pacStack.push((successor[0], currentState[1] + (successor[1],)))

    return list(currentState[1])

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    pacQueue = util.Queue()
    visited = []
    currentState = problem.getStartState()
    pacQueue.push((currentState, ()))
    visited.append(currentState)
    currentState = pacQueue.pop()

    while not problem.isGoalState(currentState[0]):
        for successor in problem.getSuccessors(currentState[0]):
            success = True
            if successor[0] in visited:
                success = False
            if success:
                pacQueue.push((successor[0], currentState[1] + (successor[1],)))
                visited.append(successor[0])
        currentState = pacQueue.pop()
    return list(currentState[1])
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pacPrior = util.PriorityQueue()
    visited = []
    currentState = problem.getStartState()
    pacPrior.push((currentState, (), 0), 0)
    visited.append((currentState, 0))
    currentState = pacPrior.pop()

    while not problem.isGoalState(currentState[0]):
        for successor in problem.getSuccessors(currentState[0]):
            success = True
            for already in visited:
                if successor[0] == already[0]:
                    if (currentState[2] + successor[2]) < already[1]:
                        pacPrior.update((successor[0], currentState[1] + (successor[1],), currentState[2]+successor[2]),
                                        currentState[2]+successor[2])
                    success = False
                    break
            if success:
                pacPrior.push((successor[0], currentState[1] + (successor[1],), currentState[2]+successor[2]),
                              currentState[2]+successor[2])
                visited.append((successor[0], currentState[2]+successor[2]))
        currentState = pacPrior.pop()
    return list(currentState[1])
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pacPrior = util.PriorityQueue()
    visited = []
    currentState = problem.getStartState()
    pacPrior.push((currentState, (), 0), heuristic(currentState, problem))
    visited.append((currentState, heuristic(currentState, problem)))
    currentState = pacPrior.pop()

    while not problem.isGoalState(currentState[0]):
        for successor in problem.getSuccessors(currentState[0]):
            success = True
            for already in visited:
                if successor[0] == already[0]:
                    if (currentState[2] + successor[2] + heuristic(currentState[0], problem)) < already[1]:
                        pacPrior.update(
                            (successor[0], currentState[1] + (successor[1],), currentState[2] + successor[2]),
                            currentState[2] + successor[2] + heuristic(successor[0], problem))
                    success = False
                    break
            if success:
                pacPrior.push((successor[0], currentState[1] + (successor[1],), currentState[2] + successor[2]),
                              currentState[2] + successor[2] + heuristic(successor[0], problem))
                visited.append((successor[0], currentState[2] + successor[2] + heuristic(successor[0], problem)))
        currentState = pacPrior.pop()
    return list(currentState[1])
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
