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
    "*** YOUR CODE HERE ***"
    """
    @:Parameter:
        ParentMap   -> A dictionary that stores the parent of a child node,used to keep track of the path
        visitedList -> A set of nodes visited in the tree
        start       -> The coordinates of Start state
        startNode   -> The tuple describing the node coordinates, direction and cost
        frontier    -> The leaf node being explored at present
        successor   -> A successor node of the frontier
        stack       -> Used to keep track of frontier and the nodes to be explored
        stackPath   -> Used to print out the final path to the goal state
    @:Function:
        Each node to be explored is popped from the stack and if its not a goal node, its unvisited successors are
        pushed into the stack. This continues until either the goal node is reached or stack is empty [no goal node].
        ParentMap is updated as the tree is traversed. The stackPath returns the list of actions taken to reach goal
        from startnode.
    """
    parentMap = {}
    visitedList = set()
    start = problem.getStartState()
    startNode = (start,'start',0)
    stack = util.Stack()
    stack.push(startNode)
    stackpath = util.Stack()

    while not stack.isEmpty():
        frontier = stack.pop()
        visitedList.add(frontier[0])

        if not problem.isGoalState(frontier[0]):
            for successors in problem.getSuccessors(frontier[0]):
                parentMap[successors] = frontier
                if successors[0] not in visitedList:
                    stack.push(successors)
        else:
            break

    while frontier and frontier[1] != 'start':
        stackpath.push(frontier[1])
        frontier = parentMap[frontier]
    stackpath.list.reverse()

    return stackpath.list
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"
    """
    @:Parameter:
        visitedList -> A set of nodes visited in the tree
        start       -> The coordinates of Start state
        startNode   -> The tuple describing the node coordinates, direction and cost
        queue       -> Stores lists of nodes indicating the paths that are left to be explored in order to find the goal
        path        -> The list of nodes showing the path being explored in the current iteration
        frontier    -> The leaf node of the path being explored in the current iteration
        successor   -> A successor node of the frontier
        newPath     -> The path being explored with one successor of the frontier
    @:Function:
        Each path to be explored is popped from the priorityQueueWithFunction (with length being its priority function) and
        if its leaf node is not a goal node,each of its unvisited successor is added to the current path and pushed into the
         Queue one at a time. This continues until either the goal node is reached or queue is empty [no goalnode].
         Once the goal node is reached, the entire list of actions/directions stored in the queue is returned.
    """

    visitedList = set()
    start = problem.getStartState()
    startNode = [(start, 'start', 0)]
    queue = util.PriorityQueueWithFunction(len)
    queue.push(startNode)
    visitedList.add(start)

    while not queue.isEmpty():
        path = queue.pop()
        frontier = path[len(path)-1]
        if problem.isGoalState(frontier[0]):
            return [node[1] for node in path][1:]
        for successors in problem.getSuccessors(frontier[0]):
            if successors[0] not in visitedList:
                visitedList.add(successors[0])
                newPath = path[:]
                newPath.append(successors)
                queue.push(newPath)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    @:Parameter:
        priorityQ   -> Used to keep track of frontier and the nodes to be explored and prioritized based on the cost of reaching it
        ParentMap   -> A dictionary that stores the parent of a child node,used to keep track of the path
        visitedList -> A set of nodes visited in the tree
        start       -> The coordinates of Start state
        startNode   -> The tuple describing the node coordinates, direction and cost
        frontier    -> The leaf node being explored at present
        successor   -> A successor node of the frontier
        Qpath       -> used to display the final path from start to goal node
    @:Function:
        Each node to be explored is popped from the Queue and if its not a goal node, its unvisited successors are
        pushed into the Queue. This continues until either the goal node is reached or stack is empty [no goalnode].
        ParentMap is updated as the tree is traversed. PriorityQueue takes node cost as its priority.
        The QPath returns the list of actions taken to reach goal from start node.
    """
    priorityQ = util.PriorityQueue()
    start = problem.getStartState()
    startNode = (start, "start", 0)
    parentMap = {}
    visitedSet = set()
    Qpath = util.Queue()
    priorityQ.push(startNode, startNode[2])

    while not priorityQ.isEmpty():
        frontier = priorityQ.pop()

        if not problem.isGoalState(frontier[0]):
            if frontier[0] not in visitedSet:
                for successor in problem.getSuccessors(frontier[0]):
                    visitedSet.add(frontier[0])
                    if successor[0] not in visitedSet:
                        lst = list(successor)
                        lst[2] += frontier[2]
                        successor = tuple(lst)
                        parentMap[successor] = frontier
                        priorityQ.update(successor,successor[2])

        else:
            break

    while frontier[1] != 'start':
        Qpath.push(frontier[1])
        frontier = parentMap[frontier]

    return Qpath.list
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
    """
    @:Parameter:
        priorityQ   -> Used to keep track of frontier and the nodes to be explored and prioritized based on the cost of reaching it
        ParentMap   -> A dictionary that stores the parent of a child node,used to keep track of the path
        visitedList -> A set of nodes visited in the tree
        start       -> The coordinates of Start state
        startNode   -> The tuple describing the node coordinates, direction and cost
        frontier    -> The leaf node being explored at present
        successor   -> A successor node of the frontier
        Qpath       -> used to display the final path from start to goal node
    @:Function:
        Each node to be explored is popped from the stack and if its not a goal node, its unvisited successors are
        pushed into the stack. This continues until either the goal node is reached or stack is empty [no goalnode].
        ParentMap is updated as the tree is traversed. PriorityQueue takes node cost as its priority.
        The QPath returns the list of actions taken to reach goal from start node.
    """

    priorityQ = util.PriorityQueue()
    start = problem.getStartState()
    startNode = (start, "start", 0)
    parentMap = {}
    visitedSet = set()
    Qpath = util.Queue()
    priorityQ.push(startNode, startNode[2])

    while not priorityQ.isEmpty():
        frontier = priorityQ.pop()

        if not problem.isGoalState(frontier[0]):
            if frontier[0] not in visitedSet:
                for successor in problem.getSuccessors(frontier[0]):
                    visitedSet.add(frontier[0])
                    if successor[0] not in visitedSet:
                        lst = list(successor)
                        lst[2] += frontier[2]
                        lst[2] += heuristic(successor[0],problem)
                        if frontier[0] != start:
                            lst[2] -= heuristic(frontier[0],problem)
                        successor = tuple(lst)
                        parentMap[successor] = frontier
                        priorityQ.update(successor, successor[2])

        else:
            goalnode = frontier
            break

    while goalnode[1] != 'start':
        Qpath.push(goalnode[1])
        goalnode = parentMap[goalnode]

    return Qpath.list
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch