from random import randint, sample, uniform
from math import floor, ceil

def takeRandom(pebbles):
    takeStack = randint(0, len(pebbles) - 1)
    takeNum = randint(1, pebbles[takeStack])
    return takeStack, takeNum

def nim(pebbles, pathOptions, playerFunk):
    totalPebbles = sum(pebbles)
    iterations = 0
    taken = 0
    choiceNdx = 0
    #print('Running nim with path options {0}'.format(pathOptions))
    while taken < totalPebbles:
        iterations += 1
        # if the chosen stack has been depleted, we need to reselect
        # There are a few options, the simplest is just to work mod
        # the length of the pebbles array
        # This relies on popping any emptied stacks
        # Popping vs leaving 0 height stacks will change how the algorithm evolves
        takeStack = (pathOptions[choiceNdx][0]) % len(pebbles)
        # We could also reselect randomly, shift by one, etc, but we will keep it simple for now

        takeNum = pathOptions[choiceNdx][1]
        #print('Trying to take {1} pebbles from stack {0} in {2}'.format(takeStack, takeNum, pebbles))
        if pebbles[takeStack] <= takeNum:
            takeNum = pebbles[takeStack]
        # Remove the taken pebbles
        pebbles[takeStack] -= takeNum
        # If the pile is empty, remove it
        if pebbles[takeStack] == 0:
            pebbles.pop(takeStack)
        taken += takeNum
        # Did we win?
        if taken >= totalPebbles:
            return 0, iterations
        
        # Unlike single stack, the opponent choice is non-trivial
        takeStack, takeNum = playerFunk(pebbles)
        # If we update the pile compensation method, we need to update it here too
        takeStack = takeStack % len(pebbles)
        if pebbles[takeStack] <= takeNum:
            takeNum = pebbles[takeStack]
        # Remove the taken pebbles
        pebbles[takeStack] -= takeNum
        # If the pile is empty, remove it
        if pebbles[takeStack] == 0:
            pebbles.pop(takeStack)
        # Did we win?
        taken += takeNum
        if taken >= totalPebbles:
            return 1, iterations
        choiceNdx += 1
        #print('Finished iteration {0}'.format(choiceNdx))
    return 1, iterations

############################
# Players to train against
############################

# Random selection
def playerRandom(pebbles):
    stack, take = takeRandom(pebbles)
    return stack, take

# This player always chooses the maximum possible value
def playerMax(pebbles):
    # Requires walking the array twice, but the array should be very short
    take = max(pebbles)
    stack = pebbles.index(take)
    return stack, take

def playerBest(pebbles):
    nimsum = 0
    # Get the nimsum (XOR) of all the stacks
    for stack in pebbles:
        nimsum = nimsum ^ stack
    # If the nimsum is zero, find a stack which, when XORed with nimsum, is less than the stack
    # If it is, we want to reduce the stack to the result of the XOR
    if nimsum != 0:
        for stack in pebbles:
            stackNimsum = nimsum ^ stack
            if stackNimsum < stack:
                return pebbles.index(stack), stack 
    # If nimsum is 0, choose randomly
    else:
        stack, take = takeRandom(pebbles)
        return stack, take

def player1():
    return [0, 1]

############################
# Mutation Functions
############################

def mutateChild(child, numOfMutations, pebbles):
    for mutations in range(0, numOfMutations+1):
        ndx = randint(0, len(child)-1)
        stack, take = takeRandom(pebbles)
        child[ndx] = [stack, take]
    return child

def mutateGene(child, mutationRate, pebbles):
    chancePerGene = mutationRate / len(child)
    for ndx, gene in enumerate(child):
        if (uniform(0.0, 1.0) < chancePerGene):
            stack, take = takeRandom(pebbles)
            child[ndx] = [stack, take]
    return child

############################
# Propagation Functions
############################

def geneticAlg(winHistory, loseHistory, numKids, counter):
    counter += 1

    # Get sets of unique random indices from both winners and losers
    # Winners are selected for reproduction
    kidIndices = sample(range(len(loseHistory)), numKids)
    # Losers are selected for... replacement
    parentalUnitIndices = sample(range(len(winHistory)), numKids)
    for i in range(0, numKids // 2):
        # A very Betan reproduction. One individual may serve as both parents
        ndx = parentalUnitIndices.pop()
        parent1 = winHistory[ndx]
        ndx = parentalUnitIndices.pop()
        parent2 = winHistory[ndx]

        # Reproduction
        child1Beg = parent1[:len(parent1)//2]
        child1End = parent1[len(parent1)//2:]
        child2Beg = parent2[:len(parent2)//2]
        child2End = parent2[len(parent2)//2:]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        
        # Replacement
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild1
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild2
    # Combine the winners with the evolved population
    pathOptions = winHistory + loseHistory
    return pathOptions, counter

def geneticAlgWithSingleMutation(winHistory, loseHistory, numKids, mutationRate, counter, pebbles):
    counter += 1
    # Get sets of unique random indices from both winners and losers
    # Winners are selected for reproduction
    kidIndices = sample(range(len(loseHistory)), numKids)
    # Losers are selected for... replacement
    parentalUnitIndices = sample(range(len(winHistory)), numKids)
    for i in range(0, numKids // 2):
        # A very Betan reproduction. One individual may serve as both parents
        ndx = parentalUnitIndices.pop()
        parent1 = winHistory[ndx]
        ndx = parentalUnitIndices.pop()
        parent2 = winHistory[ndx]

        # Reproduction
        child1Beg = parent1[:len(parent1)//2]
        child1End = parent1[len(parent1)//2:]
        child2Beg = parent2[:len(parent2)//2]
        child2End = parent2[len(parent2)//2:]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        
        mutate1 = randint(0, 100)
        if mutate1 < mutationRate:
            #print("mutation child1 Single")
            newChild1 = mutateChild(newChild1, 1, pebbles)
        mutate2 = randint(0, 100)
        if mutate2 < mutationRate:
            #print("mutation child2 Single")
            newChild2 = mutateChild(newChild2, 1, pebbles)

        # Replacement
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild1
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild2
    # Combine the winners with the evolved population
    pathOptions = winHistory + loseHistory
    return pathOptions, counter

def geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, mutationRate, counter, pebbles):
    counter += 1
    # Get sets of unique random indices from both winners and losers
    # Winners are selected for reproduction
    kidIndices = sample(range(len(loseHistory)), numKids)
    # Losers are selected for... replacement
    parentalUnitIndices = sample(range(len(winHistory)), numKids)
    for i in range(0, numKids // 2):
        # A very Betan reproduction. One individual may serve as both parents
        ndx = parentalUnitIndices.pop()
        parent1 = winHistory[ndx]
        ndx = parentalUnitIndices.pop()
        parent2 = winHistory[ndx]

        # Reproduction
        child1Beg = parent1[:len(parent1)//2]
        child1End = parent1[len(parent1)//2:]
        child2Beg = parent2[:len(parent2)//2]
        child2End = parent2[len(parent2)//2:]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        
        #print("mutation child1 Multiple")
        mutateGene(newChild1, mutationRate, pebbles)
        mutateGene(newChild2, mutationRate, pebbles)

        # Replacement
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild1
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild2
    # Combine the winners with the evolved population
    pathOptions = winHistory + loseHistory
    #return pathOptions, counter
    return counter


def battle(pathOptions, pebbles, playerFunk):
    wins = 0
    for i in range(0, len(pathOptions)):
        #print('calling nim in BATTLE with path options {0}'.format(pathOptions))
        winner, iterations = nim(pebbles, pathOptions[i], playerFunk)
        if winner == 0:
            wins += 1
    return wins

def resetPebbles(pebbles, values):
    pebbles = []
    for value in values:
        pebbles.append(value)
    return pebbles

def main():
    # pebbles and pebbleValues should have the same values initially
    pebbles = [31, 41, 59]
    pebbleValues = []
    generationSize = 1000
    reproductionRate = 0 #.2
    mutationRate = 0 #.1
    generations = 0
    winHistory = []
    loseHistory = []
    pathOptions = []
    trainingPlayer = playerRandom
    desiredWinRate = .90
    
    stacks = len(pebbles)
    totalPebbles = sum(pebbles)
    for value in pebbles:
        pebbleValues.append(value)
    for i in range(0, generationSize):
        pebbles = resetPebbles(pebbles, pebbleValues)
        baseline = []
        # Need to give nim a random array that guarantees all the pebbles get taken
        # An array with totalPebbles / 2 elements should guarantee this.
        for foo in range(totalPebbles // 2):
            randStack = randint(0, stacks-1)
            #print('In baseline, randStack = {0}'.format(randStack))
            randTake = randint(1, pebbles[randStack])
            baseline.append([randStack, randTake])
        # print('calling nim for BASELINE with path options {0}'.format(baseline))
        winner, iterations = nim(pebbles, baseline, trainingPlayer)
        print('Baseline winner: {0}'.format(winner))
        if winner == 0:
            #print('Winning baseline: {0}'.format(baseline[0:iterations]))
            winHistory.append(baseline[0:iterations])
        else:
            #print('Losing baseline: {0}'.format(baseline[0:iterations]))
            loseHistory.append(baseline[0:iterations])
    print("Number baseline wins out of {0}: {1}".format(generationSize, len(winHistory)))
    winPercent = len(winHistory) / generationSize
    # Until our family gets strong enough...
    while winPercent < desiredWinRate:
        # Feed the winning paths back into evolution

        # With multiple mutations, continuous mutation scaling
        scalingMutationRate = min([0, 1 - winPercent]) * mutationRate
        #scalingReproductionRate = min([0, 1 - winPercent]) * reproductionRate
        scalingReproductionRate = reproductionRate
        numKids = min([len(winHistory), floor(len(loseHistory)*scalingReproductionRate)])
        numKids = (numKids // 2) * 2
        #print('Win history: {0}, lose history:'.format(winHistory[0]))
        #pathOptions, generations = geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, scalingMutationRate, generations, pebbles)
        generations = geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, scalingMutationRate, generations, pebbles)
        print('pathOptions == baseline ? {0}'.format(pathOptions == baseline))
        #print('Path options after ga: {0}'.format(pathOptions[0]))
        # Clear the histories
        winHistory = []
        loseHistory = []
        # For each of the products of this round of evolution...
        for i in range(0, len(pathOptions)):
            # Have them play again
            #print('calling nim for TRAINING with pathOptions length: {0}'.format(len(pathOptions)))
            winner, iterations = nim(pebbles, pathOptions[i], trainingPlayer)
            #print('Training winner: {0}'.format(winner))
            # If player 0 wins, add them to the new win history list
            if winner == 0:
                #print('A winning strategy: {0}'.format(pathOptions[i]))
                winHistory.append(pathOptions[i][0:iterations])
            else: 
                loseHistory.append(pathOptions[i][0:iterations])
        print("Number of training wins out of {0}: {1}".format(len(pathOptions), len(winHistory)))
        # recalculate the winning percentage
        winPercent = len(winHistory) / len(pathOptions)
    print('AAA - It took {0} generations to achieve a win rate of at least {1}.'.format(generations, desiredWinRate))

    wins = battle(pathOptions, totalPebbles, playerBest)
    print("Number of battle wins out of {0} against playerBest: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, playerMax)
    print("Number of battle wins out of {0} against playerMax: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, playerRandom)
    print("Number of battle wins out of {0} against playerRandom: {1}".format(generationSize, wins))
    
main()
