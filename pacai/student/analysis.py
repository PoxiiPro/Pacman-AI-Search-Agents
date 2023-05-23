"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    I did trial and error until the agent, blue dot, would corss the bridge.
    The default .2 noise makes it go right one and then down. I tried .5, but
    the agent goes right one and up one. Then I tried noise .3 and it seems to
    go all the way down the bridge sometimes, but at least makes an attempt to
    go down the bridge every time. Then I tried smaller numbers and found that
    the smaller noise made the agent more likley to go down the bridge. 0.0 noise
    seemed to do the trick.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Prefer the close exit (+1), risking the cliff (-10):
    [.2 discount makes the agent prio the closest exit.
    0.0 no noise so it will prio an optimal path using the cliff
    0.0 living reward so it does stay away from the cliff]
    """

    answerDiscount = 0.2
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward
    # return NOT_POSSIBLE

def question3b():
    """
    Prefer the close exit (+1), but avoiding the cliff (-10):
    [.1 discount so the agent cares more about the closer goal state.
    .1 noise so it will take more optimal path
    .1 living reward so it avoids the cliff at first but can still go down
    sort of near it to reach the closest goal state]
    """

    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0.1

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    Prefer the distant exit (+10), risking the cliff (-10):
    [.9 makes the agent prio the future rewards more
    0.0 for optimal path long clif
    0.0 so it doesnt stay away from the riskier cliffside]
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward
    # return NOT_POSSIBLE

def question3d():
    """
    Prefer the distant exit (+10), avoiding the cliff (-10):
    [.9 discount so future rewards are prio more instead of the closest.
    .1 noise seemed okay for a more optimal route.
    .9 living reward so the agent avoids the clif path,]
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0.9

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    Avoid both exits (also avoiding the cliff):
    [0 discount so the agent doesnt have motive to go to a goal.
    no noise so the agent makes the more optimal paths.
    0.9 living reward so the agent stays away from the cliff and
    only focuses on living rather then going to any goal states.]
    """

    answerDiscount = 0.0
    answerNoise = 0.0
    answerLivingReward = 0.9

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [I ran the default command given and found that the agent does not make
    its way across the bridge with the defaul parameters. It reaches about half way.
    With epislon 1, it only goes one state down the bridge and then gets stuck in a loop
    of going back and forth between start state and one state down the bridge.
    Then I began a lot of trial and error. I think the epislon has to be high enough
    so the agent will explore new states, but also can't be too high or it wont be
    consistent 99% of the time. The learning rate cannot be too high so that it doesnt
    put such a high value on going back to the start state before exploring the bridge.
    Overall I don't think this perfect balance exsists.]
    """

    # answerEpsilon = .5
    # answerLearningRate = .9
    return NOT_POSSIBLE
    # return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
