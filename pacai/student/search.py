# """
# In this file, you will implement generic search algorithms which are called by Pacman agents.
# """
# Nathan Yuan
# lab1
# from pacai.core.directions import Directions
from pacai.util.stack import Stack    # import stack for DFS
from pacai.util.queue import Queue  # import q for BFS
from pacai.util.priorityQueue import PriorityQueue  # import prio q for UCS

# directory for provel functions: pacai.core.search.problem

# for my own compile testing readability
# print("\n\n\n\n\n\n NEW COMPILE OUTPUT STARTS HERE:\n")

# """
# given code to test DFS function:

# mac vers:
# python3 -m pacai.bin.pacman --layout tinyMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.depthFirstSearch

# python3 -m pacai.bin.pacman --layout mediumMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.depthFirstSearch

# python3 -m pacai.bin.pacman --layout bigMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.depthFirstSearch
# """

def depthFirstSearch(problem):
    # """
    # Search the deepest nodes in the search tree first [p 85].
    # Your search algorithm needs to return a list of actions that reaches the goal.
    # Make sure to implement a graph search algorithm [Fig. 3.7].
    # To get started, you might want to try some of these simple commands to
    # understand the search problem that is being passed in:
    # ```
    # print("Start: %s" % (str(problem.startingState())))
    # print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    # print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    # ```
    # """

    # *** Your Code Here ***

    # some code to find out whats going on :P
    # print("HELLO WORLD")
    # print("Start: %s" % (str(problem.startingState())))
    # print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    # print("Start's successors: %s" % (problem.successorStates(problem.startingState())))

    # abbreivation
    p = problem

    # stack s
    s = Stack()

    # empty list for path
    path = []

    startState = [(p.startingState()), 'None', 0]
    # print("\nStartstate:, ", startState)

    # initialize stack with starting state for LIFO DFS graph search
    s.push(startState)
    # path.append(startState[1])   # intialize path with starting state
    # print("\nStarting path, ", path)

    # initalize a list to store visited states
    vS = [startState[0]]
    # print("\nStarting visited, ", vS)

    currentState = startState
    # print("\nStarting currentState, ", currentState)

    # store the successor states of the current state
    # successors = p.successorStates(currentState[0])
    # print("\nSuccessors: ", successors)

    temptState = startState

    # dictionary to store successor states of parents so dont have
    # to call the function while backtracking
    backtrack = {}

    validState = True

    while s:    # loop to search until stack is empty

        if p.isGoal(currentState[0]):   # if the (x, y) coordinate in current state is the goal
            return path

        # exploring
        if validState is True:
            successors = p.successorStates(currentState[0])    # update sucessors
            successors = successors[::-1]   # reverse the sucessors
            # print("\nSuccessors update: ", successors)

            # backtracking, use saved list of successors
        elif validState is False:
            successors = backtrack[currentState[0]]
            # print("\nSuccessors update backtracking: ", successors)

        # store parent as key and successors as the values in dict
        backtrack[currentState[0]] = successors
        # print("\nbacktrack dictionary update: ", backtrack)

        # # to load start state inside visited
        # vS.append(currentState[0])

        # iterate thru successor states
        for state in successors:
            # print("state being checked: ", state)

            # if the state is not visited yet
            if state[0] not in vS:
                # the current state is now the new state
                currentState = state

                # this keeps track that a new path was found
                temptState = state

                # push the state onto stack
                s.push(currentState)
                # print("\nCurrent state update, ", currentState)

                # append the state to mark as visited
                vS.append(currentState[0])
                # print("\nVisited states update, ", vS)

                # update the path
                path.append(currentState[1])
                # print("\nPath update, ", path)

                # there was a valid unvisited state found out of the sucessor states
                validState = True

                # break to re enter loop with new set of sucessors for dfs
                break
            else:
                # no valid state that has not been visited had been found yet
                validState = False

        # no valid state was found out of all successor options, so backtrack
        if validState is False:
            # print("temp state: ", temptState)
            # temp state was not changed meaning no new path was found from successors so backtrack
            if temptState == currentState:
                # actually remove it since it had no new paths
                s.pop()

                # remove path
                path.pop()
                # print("\nPath update after pop, ", path)

            # pop from stack to get the prev value
            currentState = s.pop()

            # update tempState
            temptState = currentState

            # put it back, not checked for new paths yet
            s.push(currentState)
            # print("\nCurrent state after backtracking, ", currentState)

    return "Failure"

# """""
# BFS given testing commands
# python3 -m pacai.bin.pacman --layout tinyMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.breadthFirstSearch

# python3 -m pacai.bin.pacman --layout mediumMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.breadthFirstSearch

# python3 -m pacai.bin.pacman --layout bigMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.breadthFirstSearch

# python3 -m pacai.bin.eightpuzzle
# """""

def breadthFirstSearch(problem):
    # """
    # Search the shallowest nodes in the search tree first. [p 81]
    # """

    # *** Your Code Here ***

    # abbreivation
    p = problem

    # print("\nStartstate:, ", startState)
    startState = [(p.startingState()), 'None', 0]

    # queue q
    q = Queue()

    # dicitonary to back track through later to create BFS path
    parentStates = {startState[0]: None}

    # initilize list for path
    path = []

    # initialize q with starting state for FIFO BFS graph search
    q.push(startState)
    # path.append(startState[1])   # intialize path with starting state
    # print("\nStarting path, ", path)

    # initalize a list to store visited states
    vS = [startState[0]]
    # print("\nStarting visited, ", vS)

    currentState = startState
    # print("\nStarting currentState, ", currentState)

    # successors = p.successorStates(currentState[0])
    # # store the successor states of the current state
    # print("\nSuccessors: ", successors)

    # loop to search until q is empty
    while q:

        # pop first item in q
        currentState = q.pop()

        # if the (x, y) coordinate in current state is the goal
        if p.isGoal(currentState[0]):
            # print("\nGoal was reached! Begin backtracking to get path:")
            # print("\nParent dictionary: ", parentStates)

            # while the current state is not at the start of the dict
            while currentState is not None:
                path.append(currentState[1])
                # print("\npath update: ", path)

                # backtrack
                currentState = parentStates[currentState[0]]
                # print("\nnew current state for backtracking: ", currentState)

            # remove the starting space placeholder None from path
            path.pop()

            # reverse the path
            path = path[::-1]
            # print("Path being returned: ", path)
            return path

        # update sucessors
        successors = p.successorStates(currentState[0])
        # print("\nSuccessors update: ", successors)

        # update sucessors
        for state in successors:
            # print("\nstate being checked: ", state)

            # if the state is not visited yet
            if state[0] not in vS:

                # push the state onto q
                q.push(state)
                # print("\nCurrent state update, ", state)

                # append the state to mark as visited
                vS.append(state[0])
                # print("\nVisited states update, ", vS)

                parentStates[state[0]] = currentState

    return "Failure"

# """""
# UCS given testing commands
# python3 -m pacai.bin.pacman --layout tinyMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.uniformCostSearch

# python3 -m pacai.bin.pacman --layout mediumMaze --pacman SearchAgent
# --agent-args fn=pacai.student.search.uniformCostSearch

# python3 -m pacai.bin.pacman --layout mediumDottedMaze
# --pacman StayEastSearchAgent

# python3 -m pacai.bin.pacman --layout mediumScaryMaze
# --pacman StayWestSearchAgent
# """""

def uniformCostSearch(problem):
    # """
    # Search the node of least total cost first.
    # """

    # *** Your Code Here ***

    # abbreivation
    p = problem

    startState = [(p.startingState()), 'None', 0]
    # print("\nStartstate:, ", startState)

    # prio queue q
    q = PriorityQueue()

    # dicitonary to back track through later to create UCS path
    parentStates = {startState[0]: None}
    path = []  # initilize list for path

    # initialize stack with starting state for UCS and prio/cost of 0
    q.push(startState, 0)

    # initalize a list to store visited states
    vS = [startState[0]]
    # print("\nStarting visited, ", vS)

    currentState = startState
    # print("\nStarting currentState, ", currentState)

    # store the successor states of the current state
    # successors = p.successorStates(currentState[0])
    # print("\nSuccessors: ", successors)

    # dict to keep track of costs, initiliaze with start state
    stateCosts = {startState[0]: 0}

    # loop to search until q is empty
    while q:

        # pop first item in q
        currentState = q.pop()

        # if the (x, y) coordinate in current state is the goal
        if p.isGoal(currentState[0]):
            # print("\nGoal was reached! Begin backtracking to get path:")
            # print("\nParent dictionary: ", parentStates)

            # while the current state is not at the start of the dict
            while currentState is not None:
                path.append(currentState[1])
                # print("\npath update: ", path)

                # backtrack
                currentState = parentStates[currentState[0]]
                # print("\nnew current state for backtracking: ", currentState)

            # remove the starting space placeholder None from path
            path.pop()

            # reverse the path
            path = path[::-1]
            # print("Path being returned: ", path)
            return path

        # update sucessors
        successors = p.successorStates(currentState[0])
        # print("\nSuccessors update: ", successors)

        # iterate thru successor states
        for state in successors:
            # print("\nstate being checked: ", state)

            # if the state is not visited yet
            if state[0] not in vS:

                # update the cost by combining the current state price and the parents state price
                cost = stateCosts[currentState[0]] + state[2]
                # print("new cost before being added to cost list: ", cost)

                # update the cost of the state
                stateCosts[state[0]] = cost

                # push the lowest cost next state onto q and its cost/prio
                q.push(state, cost)
                # print("\nCurrent state update, ", state, cost)

                # append the state to mark as visited
                vS.append(state[0])
                # print("\nVisited states update, ", vS)

                parentStates[state[0]] = currentState

    return "Failure"

"""""
Given test code:
python3 -m pacai.bin.pacman --layout bigMaze --pacman SearchAgent
--agent-args fn=pacai.student.search.aStarSearch,heuristic=pacai.core.search.heuristic.manhattan
"""""

def aStarSearch(problem, heuristic):
    # """
    # Search the node that has the lowest combined cost and heuristic first.
    # """

    # abbreivation
    p = problem

    startState = [(p.startingState()), 'None', 0]
    # print("\nStartstate:, ", startState)

    # prio queue q
    q = PriorityQueue()

    # dicitonary to back track through later to create UCS path
    parentStates = {startState[0]: None}

    # initilize list for path
    path = []

    startCost = startState[2] + heuristic(startState[0], p)
    # print("\nStart cost + heurisitc: ", startCost)

    # initialize stack with starting state for UCS and prio/cost of 0
    q.push(startState, startCost)

    # initalize a list to store visited states
    vS = [startState[0]]
    # print("\nStarting visited, ", vS)

    currentState = startState
    # print("\nStarting currentState, ", currentState)

    # store the successor states of the current state
    # successors = p.successorStates(currentState[0])
    # print("\nSuccessors: ", successors)

    # dict to keep track of costs, initiliaze with start state
    # stateCosts = {startState[0]: 0}

    # loop to search until q is empty
    while q:

        # pop first item in q
        currentState = q.pop()

        # if the (x, y) coordinate in current state is the goal
        if p.isGoal(currentState[0]):
            # print("\nGoal was reached! Begin backtracking to get path:")
            # print("\nParent dictionary: ", parentStates)

            # while the current state is not at the start of the dict
            while currentState is not None:
                path.append(currentState[1])
                # print("\npath update: ", path)

                # backtrack
                currentState = parentStates[currentState[0]]
                # print("\nnew current state for backtracking: ", currentState)

            # remove the starting space placeholder None from path
            path.pop()

            # reverse the path
            path = path[::-1]
            # print("Path being returned: ", path)
            return path

        # update sucessors
        successors = p.successorStates(currentState[0])
        # print("\nSuccessors update: ", successors)

        # iterate thru successor states
        for state in successors:
            # print("\nstate being checked: ", state)

            # if the state is not visited yet
            if state[0] not in vS:

                # update the cost by combining the current state cost and the heurisitc
                cost = state[2] + heuristic(state[0], p)
                # print("new cost before being added to cost list: ", cost)

                # update the cost of the state
                # stateCosts[state[0]] = cost

                # push the lowest cost next state onto q and its cost/prio
                q.push(state, cost)
                # print("\nCurrent state update, ", state, cost)

                # append the state to mark as visited
                vS.append(state[0])
                # print("\nVisited states update, ", vS)

                parentStates[state[0]] = currentState
    return "Failure"
