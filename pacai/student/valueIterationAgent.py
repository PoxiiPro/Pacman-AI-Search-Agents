from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        self.prevValues = {}

        # Compute the values here:
        # print("\n__init__\n")
        # print("init - iterations: ", iters)

        states = self.mdp.getStates()
        # print("init - states before edit: ", states)

        # states.pop(0)
        # states.append('TERMINAL_STATE')
        # print("init - states after edit: ", states)

        # qValList = []
        # bestQVal = -88888
        # qVal = 0

        # initialize the dicts to 0
        for state in states:
            self.values[state] = 0
            # self.prevValues[state] = 0

        # start value iteration:
        for i in range(self.iters):
            # make a copy of the current values to store as prev values for later
            prevValues = self.values.copy()

            # update the value of each state
            for state in self.mdp.getStates():
                # if state is a temrinal state
                if self.mdp.isTerminal(state):
                    # terminal states have a value of 0
                    prevValues[state] = 0
                # else not a temrminal state
                else:
                    # calculate the q vals for each action and then update the value of the state
                    qVal = 0
                    bestQVal = -88888
                    possibleActions = self.mdp.getPossibleActions(state)
                    # print("init - possibleActions: ", possibleActions)

                    # iterate thru possible actions to find best q val
                    for action in possibleActions:
                        qVal = self.getQValue(state, action)
                        # get best q val using max between the two
                        bestQVal = max(bestQVal, qVal)
                    prevValues[state] = bestQVal

            # update the prev values
            self.values = prevValues

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
        The q-value of the state action pair (after the indicated number of value iteration passes).
        Note that value iteration does not necessarily create this quantity,
        and you may have to derive it on the fly.
        """
        # print("\ngetQValue\n")

        # q val initialized to 0
        qVal = 0

        # list to hold values and later sum
        qValList = []

        tStates = self.mdp.getTransitionStatesAndProbs(state, action)
        # print("getQValue - tStates ", tStates)

        # loop through and calculate expected discount of future rewards
        for tState in tStates:
            # # list to hold values and later sum
            # qValList = []

            # unpack the next state and probability
            nextState, T = tState
            # print("getQValue - next state: ", nextState, "and probability: ", T)

            # get the future reward for the next state, action, nextState transition
            futureR = self.mdp.getReward(state, action, nextState)
            # print("getQValue - current reward: ", R)

            # get next value
            Vstar = self.getValue(nextState)
            # print("getQValue - value of next state: ", Vstar)

            discountLambda = self.discountRate
            # print("getQValue - lambda: ", discountLambda)

            qValList.append(T * (futureR + discountLambda * Vstar))
            # print("getQValue - qValList update: ", T * (R + (discountLambda * Vstar)))
            # print("getQValue - qValList: ", qValList)

        # get the sum
        qVal = sum(qValList)
        # print("getQValue - qVal: ", qVal)

        # update the state-action value in the dictionary
        # self.prevValues[(state, action)] = qVal
        # print("getPolicy - prev values dict update: ", self.prevValues)

        return qVal

    def getPolicy(self, state):
        """
        `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        # print("\ngetPolicy\n")
        possibleActions = self.mdp.getPossibleActions(state)

        # Note that if there are no legal actions, which is the case at the terminal state,
        # you should return None
        if len(possibleActions) == 0:
            return None

        # initalize best action and qval
        bestAction = None
        bestQVal = -888888
        qVal = 0

        # loop through all possible actions and get their q values
        for action in possibleActions:
            qVal = self.getQValue(state, action)
            # print("getPolicy - action: ", action, " q val: ", qVal)

            # check to see if best policy needs to be updated
            # You may break ties any way you see fit
            if qVal >= bestQVal:
                bestQVal = qVal
                bestAction = action

        policy = bestAction
        # print("getPolicy - optimal policy: ", policy)

        return policy
