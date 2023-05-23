"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

# Nathan Yuan
# Lab1

import logging

from pacai.core.actions import Actions
# from pacai.core.search import heuristic
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent

from pacai.core.directions import Directions
from pacai.student.search import breadthFirstSearch

# from pacai.core.search.food import FoodSearchProblem

from pacai.student.search import uniformCostSearch
# from pacai.student.search import aStarSearch

# from pacai.util.queue import Queue


# import math

# DEFAULT_COST_FUNCTION = lambda x: 1

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```

    python3 -m pacai.bin.pacman --layout tinyCorners --pacman SearchAgent --agent-args
    fn=pacai.student.search.breadthFirstSearch,prob=pacai.student.searchAgents.CornersProblem

    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        # self.costFn = costFn

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***

    # function to return starting state
    def startingState(self):
        # return (self.startingPosition)
        # print("\nStart state (pos and unvisisted corners): ", self.startingPosition, self.corners)

        # Hint: The only parts of the game state you need to reference in your implementation
        # are the starting Pac-Man position and the location of the four corners.
        # state is starting postion and list of corners to easily keep track of goal state
        return (self.startingPosition, self.corners)

    # function to check if at goal state
    # goal state is all cornered visited in this case
    def isGoal(self, state):
        # print("\n   what is the state: ", state)
        # put the state (x, y) into current state and the list of corners into unvisited
        # currentState = state[0]
        unvisitedCorners = state[1]
        # print("\ncurrentState and list of unvisted corners: ", currentState, unvisitedCorners)

        # list to hold the corners not yet visited from the state
        # unvisitedCorners = []

        # loop through each corner to see if it has been visited
        # for corner in self.corners:
        #     if corner not in self._visitHistory:
        #         unvisitedCorners.append(corner)

        # if the current state is an unvisited corner then mark it as visited
        # if currentState in unvisitedCorners:
        #     self._visitHistory.append(currentState)

        # if there are any unvisited corners then goal is not reached
        if len(unvisitedCorners) > 0:
            return False

        # Register the locations we have visited.
        # This allows the GUI to highlight them.
        self._visitedLocations.add(state)
        # Note: visit history requires xy coordinates not states
        coordinates = state[0]
        self._visitHistory.append(coordinates)

        # all corners have been visited so goal state has been reached
        if len(unvisitedCorners) == 0:
            return True

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a constant cost of 1.
        """

        currentState = state[0]

        # led to bug, corners kept coming back
        # unvisitedCorners = state[1]
        # print("\nunvisitedCorners at start of func: ", unvisitedCorners, "\n")

        successors = []
        # updatedUnvisitedCorners = []

        for action in Directions.CARDINAL:
            x, y = currentState
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            # print("ERROR TEST 1")

            # if you dont hit a wall
            if (not hitsWall):
                # the next state
                nextState = (nextx, nexty)

                # actual spot to place this so it doesnt keep reseting the corner list
                unvisitedCorners = state[1]

                # the next state is an unvisited corner
                if nextState in unvisitedCorners:
                    # remove the state from the unvisited corner list
                    unvisitedCorners = list(unvisitedCorners)
                    unvisitedCorners.remove(nextState)
                    # print("\nnew list of unvisited corners: ", unvisitedCorners, "\n")

                # cost of next state is 1
                cost = 1

                # print("\nnext state being added to successors: ", nextState,
                # "unvisisted corners: ", unvisitedCorners, "\n")

                # add to list of successors
                successors.append(((nextState, tuple(unvisitedCorners)), action, cost))

        # print("ERROR TEST 2")

        # Bookkeeping for display purposes (the highlight in the GUI).
        self._numExpanded += 1
        if (state not in self._visitedLocations):
            self._visitedLocations.add(state)
            # Note: visit history requires coordinates not states. In this situation
            # they are equivalent.
            coordinates = state[0]
            self._visitHistory.append(coordinates)

        # remove duplicates
        unvisitedCorners = list(set(successors))
        # print("\nsuccessors being returned: ", successors, "\n")
        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
        return len(actions)

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)

    python3 -m pacai.bin.pacman --layout mediumCorners --pacman AStarCornersAgent
    python3 -m pacai.bin.pacman --layout tinyCorners --pacman AStarCornersAgent

    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    position, unvisitedCorners = state
    # print("\nstarting position: ", position, "\n")
    # print("pos and unvisisted corners: ", state, "\n")

    # no more unvisted corners
    if len(unvisitedCorners) == 0:
        return 0

    # list to store distances
    # euclideanDistance = []
    mHDistance = []
    # mHD = []
    # mazeSearch = []
    heuristic = 0
    markedCorners = []
    cornersDict = {}

    # while not all corners have been marked
    while len(markedCorners) != len(unvisitedCorners):
        # for every unvisted corner, calculate the mh distance from position to the corner
        for corner in unvisitedCorners:
            # if the corner has not been visited yet
            if corner not in markedCorners:

                # get distance from position to corner
                mHDistance.append(abs(position[0] - corner[0]) + abs(position[1] - corner[1]))

                # add it to a dict to get the coordinate later
                cornersDict[corner] = abs(position[0] - corner[0]) + abs(position[1] - corner[1])
                # print("\ncornersDict update: ", cornersDict, "\n")

        # print("\ncornersDict after all distances have been found: ", cornersDict, "\n")

        # append smallest distance from position to nearest corner to the heuristic
        heuristic = heuristic + (min(mHDistance))
        # print("\ndistance to closest corner is: ", min(mHDistance), "\n")

        # get the x, y coords of the closest corner from the dict
        closestCornerCoords = min(cornersDict, key = cornersDict.get)
        # print("\nclosest corner is: ", closestCornerCoords, "\n")

        # update the position to the closest corner
        position = closestCornerCoords
        # print("\npostion update: ", position, "\n")

        # mark the corner as done
        markedCorners.append(closestCornerCoords)
        # print("\nvisitedCorners update: ", markedCorners, "\n")

        # reset the dict for next loop
        cornersDict = {}

        # reset the manhattanDistance for next loop
        mHDistance = []

    # print("\nheuristic being returned: ", heuristic, "\n")

    return heuristic

    # a bunch of heuristics that i tried but did not work :((
    # def cornersHeuristic(state, problem):
    # """
    # A heuristic for the CornersProblem that you defined.

    # This function should always return a number that is a lower bound
    # on the shortest path from the state to a goal of the problem;
    # i.e. it should be admissible.
    # (You need not worry about consistency for this heuristic to receive full credit.)

    # python3 -m pacai.bin.pacman --layout mediumCorners --pacman AStarCornersAgent
    # """

    # # Useful information.
    # # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # # *** Your Code Here ***

    # # print("\nwhat is the state: ", state, "\n")
    # # print("\nwhat is the problem: ", problem, "\n")

    # # These are the corner coordinates
    # # cornerCoords = problem.corners
    # # print("\ncorner coords: ", cornerCoords, "\n")

    # # euclideanDistance = 0

    # # print("\nstarting position: ", position, "\n")

    # # no more unvisted corners

    # # list to store distances
    # # euclideanDistance = []
    # manhattanDistance = []
    # # mHD = []
    # heuristic = 0
    # markedCorners = []
    # cornersDict = {}

    # # while not all corners have been visited
    # while len(markedCorners) != len(unvisitedCorners):
    #     # for every corner, calculate the mh distance from position to the corner
    #     for corner in unvisitedCorners:
    #         # if the corner has not been visited yet
    #         if corner not in markedCorners:

    #             # get distance from position to corner
    #            manhattanDistance.append(abs(position[0] - corner[0]) +
    # abs(position[1] - corner[1]))

    #             # add it to a dict to get the coordinate later
    #            cornersDict[corner] = abs(position[0] - corner[0]) + abs(position[1] - corner[1])
    #             print("\ncornersDict update: ", cornersDict, "\n")

    #     print("\ncornersDict after all distances have been found: ", cornersDict, "\n")

    #     # append smallest distance from position to nearest corner to the heuristic
    #     heuristic = heuristic + (min(manhattanDistance))
    #     print("\ndistance to closest corner is: ", min(manhattanDistance), "\n")

    #     # get the x, y coords of the closest corner from the dict
    #     closestCornerCoords = min(cornersDict, key = cornersDict.get)
    #     print("\nclosest corner is: ", closestCornerCoords, "\n")

    #     # update the postion to the closest corner
    #     position = closestCornerCoords
    #     print("\npostion update: ", position, "\n")

    #     # mark the corner as done
    #     markedCorners.append(closestCornerCoords)
    #     print("\nvisitedCorners update: ", markedCorners, "\n")

    #     # reset the dict for next loop
    #     cornersDict = {}

    #     # reset the manhattanDistance for next loop
    #     manhattanDistance = []

    # All my different heuristic attempts:
    # print("\nhello world\n")
    # print("\nstate: ", state, "corner: ", corner, "\n")

    # given heuristic function kept bugging
    # eDistance.append(heuristic.euclidean(state, (corner))

    # used more standard math method
    # realized this distance method might not be addmissable
    # eDistance.append(abs(position[0] - corner[0]) + abs(position[1] - corner[1]))

    # closestCorner = min(manhattanDistance)

    # if len(manhattanDistance) > 0:
    #     closestCornerUpdate = min(manhattanDistance)

    # # the distance that was just calculated is the new smallest
    # if closestCornerUpdate < closestCorner:
    #     closestCornerCoords = corner

    # print("\ncornersDict: ", cornersDict, "\n")

    # print("\nheuristic: ", euclideanDistance, "\n")

    # if len(manhattanDistance) > 0:
    #     closestCorner = min(manhattanDistance)
    #     unvisitedCorners = list(unvisitedCorners)
    #     unvisitedCorners.remove(closestCornerCoords)
    #     position = closestCornerCoords
    #     unvisitedCorners = tuple(unvisitedCorners)

    # closestCornerCoords = min(cornersDict, key = cornersDict.get)
    # unvisitedCorners = list(unvisitedCorners)
    # unvisitedCorners.remove(closestCornerCoords)
    # unvisitedCorners = tuple(unvisitedCorners)

    # if there are still unvisted corners remaining
    # if len(manhattanDistance) > 0:
    #     # get the closest corner not yet visited
    #     closestCorner = min(manhattanDistance)

    # loop through the other unvisted corners to get the next closest
    # for corner in unvisitedCorners:
    #     # if the corner is not visited
    #     if corner != closestCornerCoords:
    #         mHD.append(abs(closestCornerCoords[0] - corner[0]) +
    # abs(closestCornerCoords[1] - corner[1]))

    # if there is a corner still
    # if len(manhattanDistance) > 0:
    # heuristic = sum(manhattanDistance)
    # heuristic = min(manhattanDistance) + max(manhattanDistance)

    # closestCornerCoords = min(cornersDict, key = cornersDict.get)
    # closestCorner = min(manhattanDistance)
    # print("\nclosestCornerCoords: ", closestCornerCoords, "\n")
    # print("\nclosest Corner distance: ", closestCorner, "\n")

    # remove the closest corners
    # unvisitedCorners = list(unvisitedCorners)
    # unvisitedCorners.remove(closestCornerCoords)
    # unvisitedCorners = tuple(unvisitedCorners)

    # position = closestCornerCoords

    # loop to get distance from closest corner to all other corners
    # for corner in unvisitedCorners:
    #    if corner != closestCornerCoords:
    #         mHD.append(abs(closestCornerCoords[0] - corner[0]) +
    # abs(closestCornerCoords[1] - corner[1]))

    # print("\nlist of distances from closest corner to all corners: ", mHD, "\n")

    # closest corner distance from state + farthest corner distance from that corner

    # if there are other unvisted corners
    # if len(mHD) > 0:
    #     heuristic = closestCorner + max(mHD)
    # else:
    #     heuristic = 0

    # heuristic = min(manhattanDistance)

    # heuristic = sum(heuristic)
    # print("\nheuristic: ", heuristic , "\n")

    # else:
    #     heuristic = 0
    # return heuristic.null(state, problem)  # Default to trivial solution

    # if len(heuristic) > 0:
    #    return sum(heuristic)
    # else:
    # print("\nheuristic being returned: ", heuristic, "\n")

    # return heuristic

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    position, foodGrid = state
    # print("\npos to calc h for : ", position, "\n")

    # *** Your Code Here ***
    foodStates = foodGrid.asList()
    # print("\nfood states: ", foodStates, "\n")

    heuristic = 0

    mazeDistances = []
    foodDict = {}

    # there is no food
    if len(foodStates) == 0:
        return 0

    # loop through all the food on the map
    for food1 in foodStates:
        # loop through all food on the map and compute distance from each food to one another
        for food2 in foodStates:

            p = PositionSearchProblem(problem.startingGameState, start = food1, goal = food2)

            # key is a tuple of food1 and food2, value is their path distance from one another
            foodDict[food1, food2] = (len(breadthFirstSearch(p)))

    # print("\nfoodDict: ", foodDict, "\n")

    # get the farthest distanced fruits
    farthestFruits = max(foodDict, key = foodDict.get)

    # store the biggest distance
    farthestFruitsDis = foodDict[farthestFruits]

    # find the closest fruit out of the two farthest fruits
    for food3 in farthestFruits:
        p = PositionSearchProblem(problem.startingGameState, start = position, goal = food3)
        mazeDistances.append(len(uniformCostSearch(p)))
        distance = min(mazeDistances)

    # print(distance)
    # print(farthestFruitsDis)

    # add the distances
    heuristic = distance + farthestFruitsDis

    # print("\nheuristic: ", heuristic, "for pos: ", position, "\n")
    return heuristic

# a bunch of heuristics i tried that did not work:

#     position, foodGrid = state
#     print("\npos to calc h for : ", position, "\n")

#     # *** Your Code Here ***
#     foodStates = foodGrid.asList()
#     print("\nfood states: ", foodStates, "\n")

#     heuristic = 0

#     mazeDistances = []

#     # there is no food
#     # if len(foodStates) == 0:
#     #     return 0

#     # loop through all the food on the map
#     for food in foodStates:
#         # print("\nFood being calculated: ", food, "\n")

#         p = PositionSearchProblem(problem.startingGameState, start = position, goal = food)
#         # mazeDistances.append(len(uniformCostSearch(p)))
#         mazeDistances.append(len(breadthFirstSearch(p)))

#         # distance = (mazeDistance(position, food, gameState))
#         # print("\nDistance: ", distance, "\n")

#         # mazeDistances.append(len(uniformCostSearch(p))

#         # if distance > heuristic:
#         #     heuristic = distance

#         heuristic = max(mazeDistances)

#     # if len(mazeDistances) > 0:
#     #     heuristic = min(mazeDistances)

#     print("\nheuristic: ", heuristic, "for pos: ", position, "\n")
#     return heuristic

# def foodHeuristic(state, problem):

    # position, foodGrid = state
    # print("\nstate test: ", state, "\n")

    # *** Your Code Here ***
    # foodStates = foodGrid.asList()
    # print("\nfood states test: ", foodStates, "\n")

    # manhattanDistance = []

    # list to keep track of food pacman has already eaten / visited
    # eatenFood = []

    # foodDict = {}
    # mHD = []

    # mazeDistance = []
    # heuristic = -1

    # for food in foodStates:
    # if the food is not eaten/visited yet
    # if food not in eatenFood:

    # print("\nfood state: ", food, "\n")

    # use manhattan distance because it is usually admissible and consistent
    # heuristic function kept bugging
    # manhattanDistance = max(manhattanDistance, heuristic.manhattan(position, food))

    # append the distance from state to all food
    # manhattanDistance.append(abs(position[0] - food[0]) + abs(position[1] - food[1]))

    # foodDict[food] = abs(position[0] - food[0]) + abs(position[1] - food[1])

    # print("\nmH distance test: ", heuristic, "\n")

    # mark food as visited
    # eatenFood.append(food)

    # mazeDistance.append(uniformCostSearch(problem))
    # mazeDistanceHeuristic = mazeDistance(position, food, problem.startingGameState)

    # save the max distance aka farthest food path from pos
    # if mazeDistanceHeuristic > heuristic:
    #     heuristic = mazeDistanceHeuristic

    # eatenFood = []

    # get the max of all distances from state to food aka farthest food

    # print("\nmanhattanDistances: ", manhattanDistance, "\n")

    # if there is food to be eaten
    # if len(mazeDistance) > 0:
    # heuristic = max(manhattanDistance)

    # closestCornerCoords = min(foodDict, key = foodDict.get)
    # closestCorner = min(manhattanDistance)

    # loop to get distance from closest food and farthest food from that food
    # for food in foodStates:
    #     mHD.append(abs(closestCornerCoords[0] - food[0]) + abs(closestCornerCoords[1]
    # - food[1]))

    #     # closest food distance from state + farthest food distance from that food
    #     heuristic = closestCorner + max(mHD)

    #     heuristic = max(mazeDistance)
    # else:
    #     heuristic = 0

    # return heuristic.null(state, problem)  # Default to the null heuristic.
    # return heuristic


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        # raise NotImplementedError()

        problem = AnyFoodSearchProblem(gameState)
        return breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        x, y = state

        # if current state contains a food
        if self.food[x][y] is True:
            return True
        else:
            return False

class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
