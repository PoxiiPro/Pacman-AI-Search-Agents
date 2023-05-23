# Nathan Yuan

import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.agents.capture.capture import CaptureAgent
from pacai.core import distanceCalculator

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        # print("\nnewPos: ", newPosition)
        oldFood = currentGameState.getFood()
        # print("\nfood: ", oldFood)
        newGhostStates = successorGameState.getGhostStates()
        # print("\nghostStates: ",newGhostStates)
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
        # print("\nscaredTimer: ",newScaredTimes)

        # *** Your Code Here ***
        gameStateScore = 0
        # numOfFood = currentGameState.getNumFood()
        foodGrid = oldFood.asList()

        foodList = []
        # get distance to closest food, the closer to food the better
        for food in foodGrid:
            foodList.append(abs(newPosition[0] - food[0])
            + abs(newPosition[1] - food[1]))
        # print("\nclosest food: ", min(foodList))
        foodScore = (88 - min(foodList))
        # print("\nfoodScore: ", foodScore)

        distanceToGhosts = []
        ghostScore = 0

        # if the ghosts are not scared
        if newScaredTimes[0] == 0:
            # get the manhattan distance from new pacman pos to all ghosts pos
            # the farther the closest ghost the better
            for ghost in newGhostStates:
                ghostCoords = ghost.getPosition()
                # print("\nghost: ", ghostCoords)
                distanceToGhosts.append(abs(newPosition[0] - ghostCoords[0])
                + abs(newPosition[1] - ghostCoords[1]))

            # if the closest ghost is 1 or less distance away, add a heavier weight
            # to make pacman run away
            if min(distanceToGhosts) <= 1:
                ghostScore = -8
            # this makes pacman too scared, only needs to run if ghost is really close
            # else: ghostScore = min(distanceToGhosts)

            # print("\ndistance to ghosts: ", distanceToGhosts)

        # else the ghosts are scared, then closer distance to them is good
        else:
            for ghost in newGhostStates:
                ghostCoords = ghost.getPosition()
                # print("\nghost: ", ghostCoords)
                distanceToGhosts.append(abs(newPosition[0] - ghostCoords[0])
                + abs(newPosition[1] - ghostCoords[1]))

            # print("\ndistance to scared ghosts: ", distanceToGhosts)
            ghostScore = 888 - min(distanceToGhosts)

        gameStateScore = foodScore + ghostScore

        # print("\ngame state score returned: ", gameStateScore)
        return gameStateScore

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        # print("\ngameState", gameState, "\n")

        # get the depth of the tree (how far an agent will look ahead)
        treeDepth = self.getTreeDepth()
        # print("\ngetAction - treeDepth: ", treeDepth, "\n")

        # get next possible moves from pacmans current state
        legalActions = gameState.getLegalActions(0)
        # print("\ngetAction - Legal actions: ", legalActions, "\n")

        bestAction = 'Stop'

        maxScore = -8888.88

        # agentInitiative = 0

        # loop through actions and calculate score using miniMax. Find best score/ best action
        for action in legalActions:

            # get the next possible state and set a pacman to go first
            successorState = gameState.generateSuccessor(0, action)

            # score.append(self.miniMax(successorState, treeDepth, 0))

            score = self.miniMax(successorState, treeDepth, 0)
            if score > maxScore:
                maxScore = score
                bestAction = action

        # print("\ngetAction - best action: ", bestAction,)
        # print("\ngetAction - max score: ", maxScore, "\n")

        return bestAction

    def miniMax(self, gameState, treeDepth, agentInitiative):

        # 0 is PacMans initative, any num != 0 is a ghost initiative
        # print("\nminiMax - current initiative: ", agentInitiative, "\n")

        # num of agents in game, pacman + num of ghosts
        numOfAgents = gameState.getNumAgents()
        # print("\nminiMax - num of agents: ", numOfAgents, "\n")

        # check what treeDepth is being explored right now
        # print("\nminiMax - current treeDepth: ", treeDepth, "\n")

        # reached the end of the min max tree
        if treeDepth == 0:
            return self.getEvaluationFunction()(gameState)

        # get next possible moves from agents current state
        legalActions = gameState.getLegalActions(agentInitiative)

        # terminal state was reached
        if len(legalActions) == 0:
            return self.getEvaluationFunction()(gameState)

        # print("\nminiMax - Legal actions: ", legalActions, "\n")

        minimaxNode = []

        miniMaxVal = -88888.88

        # 0 means Pacmans turn to play, and pacman is the top max node
        if agentInitiative == 0:
            # hint given said to remove stop action from Pacman
            legalActions.remove('Stop')
            # print("\nminiMax - Legal actions pacman: ", legalActions, "\n")

            for action in legalActions:
                # get the successor states for pacman and set the next turn to be a ghost
                sucessorState = gameState.generateSuccessor(0, action)
                # print("\nminiMax - sucessor state: ", sucessorState, "\n")

                # append the states to the list
                minimaxNode.append(self.miniMax(sucessorState, treeDepth, 1))
                # print("\nminiMax - max node list update, pacman: ", minimaxNode, "\n")

                # return the max
                miniMaxVal = max(minimaxNode)
                # print("\nminiMax - max val, pacman: ", miniMaxVal, "\n")
        else:   # if not pacman then its a ghost's turn, ghosts are min nodes
            for action in legalActions:
                # get the successor states and set the next turn to be next ghost
                sucessorState = gameState.generateSuccessor(agentInitiative, action)
                # print("\nminiMax - sucessor state: ", sucessorState, "\n")

                # last ghost's turn, so reduce depth and set pacman next to start next round
                if agentInitiative == numOfAgents - 1:
                    minimaxNode.append(self.miniMax(sucessorState, treeDepth - 1, 0))
                    # print("\nminiMax - max node list update, last ghost: ", minimaxNode, "\n")
                else:
                    # non last ghosts turn, append the states to the list to get min
                    # set next ghost's turn
                    minimaxNode.append(self.miniMax(sucessorState, treeDepth, agentInitiative + 1))
                    # print("\nminiMax - max node list update, a ghost: ", minimaxNode, "\n")
                # return the min
                miniMaxVal = min(minimaxNode)
                # print("\nminiMax - min val, ghost: ", miniMaxVal, "\n")
        return miniMaxVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    # same functions from miniMax class but add alphabeta pruning
    def getAction(self, gameState):
        # print("\ngameState", gameState, "\n")

        # get the depth of the tree (how far an agent will look ahead)
        treeDepth = self.getTreeDepth()
        # print("\ngetAction - treeDepth: ", treeDepth, "\n")

        # get next possible moves from pacmans current state
        legalActions = gameState.getLegalActions(0)
        # print("\ngetAction - Legal actions: ", legalActions, "\n")

        bestAction = 'Stop'

        maxScore = -8888.88

        # agentInitiative = 0

        a = maxScore
        b = 8888.88

        # loop through actions and calculate score using miniMax. Find best score/ best action
        for action in legalActions:

            # get the next possible state and set a pacman to go first
            successorState = gameState.generateSuccessor(0, action)

            # score.append(self.miniMax(successorState, treeDepth, 0))

            score = self.miniMax(successorState, treeDepth, 0, a, b)
            if score > maxScore:
                maxScore = score
                bestAction = action

            # update alpha value bc pacman is max node
            a = max(a, maxScore)

            # check for pruning
            if b <= a:
                break

        # print("\ngetAction - best action: ", bestAction,)
        # print("\ngetAction - max score: ", maxScore, "\n")

        return bestAction

    def miniMax(self, gameState, treeDepth, agentInitiative, a, b):

        # 0 is PacMans initative, any num != 0 is a ghost initiative
        # print("\nminiMax - current initiative: ", agentInitiative, "\n")

        # num of agents in game, pacman + num of ghosts
        numOfAgents = gameState.getNumAgents()
        # print("\nminiMax - num of agents: ", numOfAgents, "\n")

        # check what treeDepth is being explored right now
        # print("\nminiMax - current treeDepth: ", treeDepth, "\n")

        # reached the end of the min max tree
        if treeDepth == 0:
            return self.getEvaluationFunction()(gameState)

        # get next possible moves from agents current state
        legalActions = gameState.getLegalActions(agentInitiative)

        # terminal state was reached
        if len(legalActions) == 0:
            return self.getEvaluationFunction()(gameState)

        # print("\nminiMax - Legal actions: ", legalActions, "\n")

        minimaxNode = []

        miniMaxVal = -88888.88

        # 0 means Pacmans turn to play, and pacman is the top max node
        if agentInitiative == 0:
            # hint given said to remove stop action from Pacman
            legalActions.remove('Stop')
            # print("\nminiMax - Legal actions pacman: ", legalActions, "\n")

            for action in legalActions:
                # get the successor states for pacman and set the next turn to be a ghost
                sucessorState = gameState.generateSuccessor(0, action)
                # print("\nminiMax - sucessor state: ", sucessorState, "\n")

                # append the states to the list
                minimaxNode.append(self.miniMax(sucessorState, treeDepth, 1, a, b))
                # print("\nminiMax - max node list update, pacman: ", minimaxNode, "\n")

                # return the max
                miniMaxVal = max(minimaxNode)
                # print("\nminiMax - max val, pacman: ", miniMaxVal, "\n")

                # update the alpha value bc pacman is max node
                a = max(a, miniMaxVal)

                # check if beta is smaller then alpha, prune if so aka stop exploring
                if b <= a:
                    break

        else:   # if not pacman then its a ghost's turn, ghosts are min nodes
            for action in legalActions:
                # get the successor states and set the next turn to be next ghost
                sucessorState = gameState.generateSuccessor(agentInitiative, action)
                # print("\nminiMax - sucessor state: ", sucessorState, "\n")

                # last ghost's turn, so reduce depth and set pacman next to start next round
                if agentInitiative == numOfAgents - 1:
                    minimaxNode.append(self.miniMax(sucessorState, treeDepth - 1, 0, a, b))
                    # print("\nminiMax - max node list update, last ghost: ", minimaxNode, "\n")
                else:
                    # non last ghosts turn, append the states to the list to get min
                    # set next ghost's turn
                    minimaxNode.append(self.miniMax(sucessorState, treeDepth,
                    agentInitiative + 1, a, b))
                    # print("\nminiMax - max node list update, a ghost: ", minimaxNode, "\n")
                # return the min
                miniMaxVal = min(minimaxNode)
                # print("\nminiMax - min val, ghost: ", miniMaxVal, "\n")

                # update beta value
                b = min(b, miniMaxVal)

                # check if pruning is needed
                if b <= a:
                    break

        return miniMaxVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        # print("\ngameState", gameState, "\n")

        # get the depth of the tree (how far an agent will look ahead)
        treeDepth = self.getTreeDepth()
        # print("\ngetAction - treeDepth: ", treeDepth, "\n")

        # get next possible moves from pacmans current state
        legalActions = gameState.getLegalActions(0)
        # print("\ngetAction - Legal actions: ", legalActions, "\n")

        bestAction = 'Stop'

        maxScore = -8888.88

        # agentInitiative = 0

        # loop through actions and calculate score using expectiMax. Find best score/ best action
        for action in legalActions:

            # get the next possible state and set a pacman to go first
            successorState = gameState.generateSuccessor(0, action)

            # score.append(self.miniMax(successorState, treeDepth, 0))

            score = self.expectiMax(successorState, treeDepth, 0)
            if score > maxScore:
                maxScore = score
                bestAction = action

        # print("\ngetAction - best action: ", bestAction,)
        # print("\ngetAction - max score: ", maxScore, "\n")

        return bestAction

    def expectiMax(self, gameState, treeDepth, agentInitiative):

        # 0 is PacMans initative, any num != 0 is a ghost initiative
        # print("\nexpectiMax - current initiative: ", agentInitiative, "\n")

        # num of agents in game, pacman + num of ghosts
        numOfAgents = gameState.getNumAgents()
        # print("\nexpectiMax - num of agents: ", numOfAgents, "\n")

        # check what treeDepth is being explored right now
        # print("\nexpectiMax - current treeDepth: ", treeDepth, "\n")

        # reached the end of the min max tree
        if treeDepth == 0:
            return self.getEvaluationFunction()(gameState)

        # get next possible moves from agents current state
        legalActions = gameState.getLegalActions(agentInitiative)

        # terminal state was reached, skip turn
        if len(legalActions) == 0:
            # print("\nexpectiMax - no legal actions, terminal state\n")
            return self.getEvaluationFunction()(gameState)

        # print("\nexpectiMax - Legal actions: ", legalActions, "\n")

        expecti = []

        expectiMaxVal = -88888.88

        # 0 means Pacmans turn to play, pacman is a max node
        if agentInitiative == 0:
            # hint given said to remove stop action from Pacman
            legalActions.remove('Stop')
            # print("\nexpectiMax - Legal actions pacman: ", legalActions, "\n")

            for action in legalActions:
                # get the successor states for pacman and set the next turn to be a ghost
                sucessorState = gameState.generateSuccessor(0, action)
                # print("\nexpectiMax - sucessor state: ", sucessorState, "\n")

                # append the states to the list
                expecti.append(self.expectiMax(sucessorState, treeDepth, 1))
                # print("\nexpectiMax - max node list update, pacman: ", expecti, "\n")

                # return the max
                expectiMaxVal = max(expecti)
                # print("\nexpectiMax - max val update, pacman: ", expectiMaxVal, "\n")
        else:   # if not pacman then its a ghost's turn, ghosts are chance nodes
            for action in legalActions:

                # get the successor states and set the next turn to be next ghost
                sucessorState = gameState.generateSuccessor(agentInitiative, action)
                # print("\nexpectiMax - sucessor state: ", sucessorState, "\n")

                # p() of taking action from current state with uniform distribution
                p = 1 / len(legalActions)
                # print("\nexpectiMax - probability of selecting an action for a ghost: ", p, "\n")

                # last ghost's turn, so reduce depth and set pacman next to start next round
                if agentInitiative == numOfAgents - 1:
                    expecti.append(p * self.expectiMax(sucessorState, treeDepth - 1, 0))
                    # print("\nexpectiMax - chance node list update, last ghost: ", expecti, "\n")
                else:
                    # non last ghosts turn, append the states to the list to get min
                    # set next ghost's turn
                    expecti.append(p * self.expectiMax(sucessorState, treeDepth,
                    agentInitiative + 1))
                    # print("\nexpectiMax - chance node list update, a ghost: ", expecti, "\n")

                expectiMaxVal = sum(expecti)
                # print("\nexpectiMax - sum aka expected value, ghost: ", expectiMaxVal, "\n")
                # print("\n hello world \n")

        return expectiMaxVal

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    I programmed the evaluation function to take into account several factors
    It will have a higher weight for a shorter distance from pacmans current pos to
    nearest capsule. It will have a decent weight, but less then the capsule weight
    for a shorter distance from pacmans current pos to nearest food. Pacamn only cares
    if a ghost is close enough to make it lose so the negative weight for that is super
    large, but only if the nearest ghost's distance is within 1. This will allow pacman to run
    away. Lastly, pacman wants the best overall game score in order to win with a high score.
    To account for this I just add the game score at the end of the score calculation with no
    extra weight. When all ghosts are scared, the score is higher the closer pacman is to the
    closest ghost allowing it to chase the scared ghost and eat it. With this score set up, pacman
    will prio capsules, then eating the scared ghosts, then food, while being able to run away from
    non scared ghosts. Pacman will also consider the overall game score to try and make more
    efficient path choices.
    """
    # successorGameState = currentGameState.generatePacmanSuccessor()

    # Useful information you can extract.
    newPosition = currentGameState.getPacmanPosition()
    # print("\nnewPos: ", newPosition)
    oldFood = currentGameState.getFood()
    # print("\nfood: ", oldFood)
    newGhostStates = currentGameState.getGhostStates()
    # print("\nghostStates: ",newGhostStates)
    newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
    # print("\nscaredTimer: ",newScaredTimes)

    # *** Your Code Here ***
    gameStateScore = currentGameState.getScore()
    numOfFood = currentGameState.getNumFood()
    foodGrid = oldFood.asList()
    foodScore = 0
    foodList = []

    # get distance to closest food, the closer to food the better
    if numOfFood > 0:
        for food in foodGrid:
            foodList.append(abs(newPosition[0] - food[0])
            + abs(newPosition[1] - food[1]))
        # print("\nclosest food: ", min(foodList))
        foodScore = (100 - min(foodList))
        # print("\nfoodScore: ", foodScore)

    capsuleList = currentGameState.getCapsules()
    capsuleDistList = []
    capsuleScore = 0
    capsuleScoreBonus = 0

    if len(capsuleList) > 0:
        # get distance to closest capsule, the closer to capsule the better, better than food
        for capsule in capsuleList:
            capsuleDistList.append(abs(newPosition[0] - capsule[0])
            + abs(newPosition[1] - capsule[1]))
            # print("\ncapsuleScore: ", capsuleScore)

            # print("\nabout to eat capsule: ", newPosition, capsule)
            # encourage pacman to eat capsule
            if newPosition == capsule:
                capsuleScoreBonus = 1000

        # print("\nclosest capsule: ", min(capsuleDistList))
        capsuleScore = (105 - min(capsuleDistList)) + capsuleScoreBonus

    distanceToGhosts = []
    ghostScore = 0
    scaredGhostCount = 0

    for ghostState in newScaredTimes:
        if ghostState > 0:
            scaredGhostCount += 1

    # if at least one ghost is not scared
    if scaredGhostCount < len(newScaredTimes) and scaredGhostCount >= 0:
        # get the manhattan distance from new pacman pos to all ghosts pos
        # the farther the closest ghost the better
        for ghost in newGhostStates:
            ghostCoords = ghost.getPosition()
            # print("\nghost: ", ghostCoords)
            distanceToGhosts.append(abs(newPosition[0] - ghostCoords[0])
            + abs(newPosition[1] - ghostCoords[1]))

        # if the closest ghost is 1 or less distance away
        # add a heavier weight to make pacman run away
        if min(distanceToGhosts) <= 1:
            ghostScore = -1000

        # this makes pacman too scared, only needs to run if ghost is really close
        # else: ghostScore = min(distanceToGhosts)

        # print("\ndistance to ghosts: ", distanceToGhosts)

    # else all the ghosts are scared, then closer distance to them is good
    elif scaredGhostCount == len(newScaredTimes):
        for ghost in newGhostStates:
            ghostCoords = ghost.getPosition()
            # print("\nghost: ", ghostCoords)
            distanceToGhosts.append(abs(newPosition[0] - ghostCoords[0])
            + abs(newPosition[1] - ghostCoords[1]))

        # print("\ndistance to scared ghosts: ", distanceToGhosts)
        ghostScore = 110 - min(distanceToGhosts)

    # the less food left the better
    # numOfFoodScore =  500 - numOfFood

    # the more the game score, the better
    # gameStateScore = gameStateScore - 500

    # the less capsules left, the better
    # numCapsulesScore = 500 - len(capsuleList)

    score = (capsuleScore) + (foodScore) + (ghostScore) + (gameStateScore - 500)
    # + (numOfFoodScore * 1) + (numCapsulesScore * 1)

    # print("\nscore breakdown: ", capsuleScore * 2, foodScore * 1, ghostScore * 1,
    # gameStateScore, numOfFoodScore, numCapsulesScore)

    # print("\ngame state score returned: ", gameStateScore)
    return score

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
