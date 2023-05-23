from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util import probability
# from pacai.core.featureExtractors import IdentityExtractor
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: my get q value method returns the q value for the current state and action
    pair. But it returns 0.0 if there is no value in the q value dict because that means it
    is not visited. My get value method uses the legal actions to find the max value out
    of the legal actions. If there are no legal actions then it is set to 0.
    getPolicy method uses legal moves and a dict to find the max val. Then uses the max val
    to return the max val's key aka action. Get action uses epislon to decide if it picks a
    random legal action or the best action. Update is in charge of updating a q state after
    calculating the new state to update it to. I did this by utilizing previous data like prev state
    and action.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.values = {}

        # print("\nHello World\n")

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        return self.values.get((state, action), 0.0)

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        # store the legal actions
        legalActions = self.getLegalActions(state)

        # Note that if there are no legal actions, which is the case at the terminal state,
        # you should return a value of 0.0.
        if len(legalActions) == 0:
            return 0.0

        # initalize a list and varibale to hold the best value out of the
        # legal actions for the state
        maxValList = []
        maxVal = -88888

        for action in legalActions:
            maxValList.append(self.getQValue(state, action))

        # get the max value of all legal action's values
        maxVal = max(maxValList)

        # # if all of the actions that your agent has seen before have a negative Q-value
        # # an unseen action may be optimal
        # if maxVal < 0:
        #     maxVal = 0

        return maxVal

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        # store the legal actions
        legalActions = self.getLegalActions(state)

        # dict to hold the legal q values
        legalValues = {}

        # Note that if there are no legal actions, which is the case at the terminal state,
        # you should return a value of None.
        if len(legalActions) == 0:
            return None

        policy = None

        # copy over the legal action q values
        for action in legalActions:
            legalValues[action] = self.getQValue(state, action)

        # get the max value of all legal action's values
        maxValKey = max(legalValues, key = legalValues.get)

        # if explored actions are negative valued
        # if all of the actions that have been seen have negative Q-values,
        # an unseen action may be optimal.

        # maxValKey = max(legalValues)

        # for key, value in legalValues.items():
        #     if value == 0:
        #         unseenAction = key

        # if legalValues[maxValKey] < 0:
        #     policy = min(legalValues, key = legalValues.get)
        unseenActions = []

        if legalValues[maxValKey] <= 0:
            for action in legalActions:
                if legalValues[action] == 0:
                    unseenActions.append(action)
            if len(unseenActions) > 0:
                return random.choice(unseenActions)

        # get the best policy action
        policy = maxValKey

        return policy

    def getAction(self, state):
        """
        Compute the action to take in the current state.
        With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
        we should take a random action and take the best policy action otherwise.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should choose None as the action.
        """
        legalActions = self.getLegalActions(state)
        # print("qlearning getAction - legealActions: ", legalActions)

        # Note that if there are no legal actions, which is the case at the terminal state,
        # you should return a value of None.
        if len(legalActions) == 0:
            return None

        p = self.getEpsilon()

        # epsilon-greedy action selection:
        # we should take a random action
        if probability.flipCoin(p) is True:
            return random.choice(legalActions)
        else:
            # and take the best policy action otherwise
            # but also consider unseen actions if all seen
            # actions are negative

            unseenActions = []

            bestAction = self.getPolicy(state)
            # if the q state val is negative or unseen
            if self.getQValue(state, bestAction) <= 0:
                for action in legalActions:
                    # if unseen state
                    if self.getQValue(state, action) == 0:
                        unseenActions.append(action)
                if len(unseenActions) > 0:
                    # print("qlearning getAction - unseenActions: ", unseenActions)
                    return random.choice(unseenActions)
            return bestAction

    def update(self, state, action, nextState, deltaReward):
        """
        The parent class calls this to observe a state transition and reward.
        You should do your Q-Value update here.
        Note that you should never call this function, it will be called on your behalf.
        """
        # store some variables for use
        prevState = self.lastState
        prevAction = self.lastAction
        disRate = self.getDiscountRate()
        a = self.alpha

        # get the max q value out of the legal states
        qVal = self.getValue(state)

        # do the calculations for the updated q value
        # put them into two parts so it still works while also
        # going with formatting reqs
        qValUpdateP1 = (1 - a) * self.getQValue(prevState, prevAction)
        qCalUpdateP2 = a * (deltaReward + disRate * qVal)
        qValUpdate = qValUpdateP1 + qCalUpdateP2

        # do the actual update on the q val
        self.values[(prevState, prevAction)] = qValUpdate

        # updates
        self.lastState = state
        self.lastAction = action

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            # print("Aprox Agent final- Weights Dict: ", self.weights)
            pass

    def getQValue(self, state, action):
        """
        Should return `Q(state, action) = w * featureVector`,
        where `*` is the dotProduct operator.
        """
        # initlaize qValues to 0 and an empty list to hold them
        qVal = 0
        qValList = []

        # get features
        # features = self.featExtractor.getFeatures(state, action)
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        # print("Aprox Agent getval - features Dict: ", features)

        if len(features) == 0:
            return qVal

        # q value calculations with features if there are
        for item in features.items():
            f, value = item
            if f in self.weights:
                qValList.append(self.weights[f] * value)
            else:
                qValList.append(0)

        qVal = sum(qValList)
        return qVal

    def update(self, state, action, nextState, deltaReward):
        """
        Should update your weights based on transition.
        """
        # store some variables for use
        # prevState = self.lastState
        # prevAction = self.lastAction
        disRate = self.getDiscountRate()
        a = self.alpha

        # get features
        # features = self.featExtractor.getFeatures(state, action)
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)

        # do the calculations for the updated q value
        qValUpdateP1 = deltaReward + disRate * self.getValue(nextState)
        qValUpdate = qValUpdateP1 - self.getQValue(state, action)

        # do the actual updating:
        for f in features:
            if f in self.weights:
                # feature is needed
                self.weights[f] += a * qValUpdate * features[f]
            else:
                # feature is not needed so its weight is 0
                self.weights[f] = 0
