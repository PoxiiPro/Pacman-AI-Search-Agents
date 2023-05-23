from pacai.agents.capture.capture import CaptureAgent
from pacai.core import directions

import random


def createTeam(firstIndex, secondIndex, isRed,

        first = 'pacai.agents.capture.dummy.DummyAgent',
        second = 'pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,|
    and will be False if the blue team is being created.
    """

    # firstAgent = reflection.qualifiedImport(first)
    # secondAgent = reflection.qualifiedImport(second)

    firstAgent = PelletCrushersOffense
    secondAgent = PelletCrushersDefense

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

# Offense Agent
class PelletCrushersOffense(CaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def evaluate(self, gameState, action):

        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features[feature] * weights[feature] for feature in features)

        return stateEval

    def getFeatures(self, gameState, action):
        features = {}
        successor = gameState.generateSuccessor(self.index, action)
        features['successorScore'] = self.getScore(successor)
        myPos = successor.getAgentState(self.index).getPosition()
        opponents = self.getOpponents(successor)
        oppsPositions = [successor.getAgentState(opps).getPosition() for opps in opponents]
        ghostStates = []
        for ghostIndex in opponents:
            currGhost = successor.getAgentState(ghostIndex)
            if currGhost.isGhost():
                ghostStates.append(currGhost)

        if successor.getAgentState(self.index).isGhost():
            for opps in oppsPositions:
                if self.getMazeDistance(myPos, opps) == 0:
                    features['copsScore'] += 1

        # Compute distance to the nearest food.
        foodList = self.getFood(gameState).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            foodDist = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = 100 - foodDist

        # make agent run away from defenders
        ghostDist = float('inf')
        ghostDistList = []
        for ghost in ghostStates:
            ghostPos = ghost.getPosition()
            ghostDistList.append(self.getMazeDistance(myPos, ghostPos))
        if (ghostDistList):
            ghostDist = min(ghostDistList)
        # if a enemy ghost is close and our attacker is a pacman (attacking)
        if ghostDist <= 1 and not gameState.getAgentState(self.index).isGhost():
            features['ghostDistance'] = ghostDist

        capsuleList = self.getCapsules(gameState)
        capsuleDist = float('-inf')
        if capsuleList:
            capsuleDist = min([self.getMazeDistance(myPos, capsule) for capsule in capsuleList])
            features['distanceToCapsule'] = 100 - capsuleDist

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': 10,
            'distanceToCapsule': 20,
            'ghostDistance': -100,
            'copsScore': 1000
        }


class PelletCrushersDefense(CaptureAgent):
    def __init__(self, index):
        super().__init__(index)

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def evaluate(self, gameState, action):
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features[feature] * weights[feature] for feature in features)

        return stateEval

    def getFeatures(self, gameState, action):
        features = {}
        successor = gameState.generateSuccessor(self.index, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        # get enemy index if they are a pacman attacking our side
        enemyAgentIndices = self.getOpponents(successor)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistanceOnOurSide'] = min(dists)

            # if there is an attacker and it is scared, dont kill it until it is brave again
            for enemyAgent in enemyAgentIndices:
                if (gameState.getAgentState(enemyAgent).isPacman()):
                    if (gameState.getAgentState(enemyAgent).isScared()):
                        if (features['invaderDistanceOnOurSide'] <= 1):
                            features['invaderDistanceOnOurSide'] = 0

        # puppy guarding
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies]
        features['invaderDistanceOnTheirSide'] = min(dists)

        if (action == directions.Directions.STOP):
            features['stop'] = 1

        rev = directions.Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistanceOnTheirSide': -10,
            'invaderDistanceOnOurSide': -50,
            'stop': -100,
            'reverse': -2
        }
