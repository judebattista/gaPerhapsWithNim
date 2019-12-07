from random import randint, sample
from math import floor

def nim(totalPebbles, maxTake, pathOptions, playerFunk):
    pullPattern = ""
    iterations = 0
    i = 0
    choiceNdx = 0
    while i < totalPebbles:
        iterations += 1
        num0 = pathOptions[choiceNdx]
        #print('num0 = {0}'.format(num0))
        pullPattern += ('0'*num0)
        i += num0
        if i >= totalPebbles:
            return 0, pullPattern, iterations
        num1 = playerFunk(maxTake, i)
        pullPattern += ('1'*num1)
        i += num1
    return 1, pullPattern, iterations
    
############################
# Players to train against
############################

# Random selection, primarily for testing trained populations
# Not a useful training tool
def playerRandom(maxTake, i):
    num0 = randint(1, maxTake)
    return num0

# This player always chooses the maximum 

def playerMax(maxTake, i):
    return maxTake

def player3(maxTake, i):
    return 3

def player2(maxTake, i):
    return 2

def player1(maxTake, i):
    return 1

def playerBest(maxTake, i):
    choice = i % (maxTake+1)
    if choice == 0:
        return maxTake
    return choice

def mutate(child, numOfMutations, maxTake):
    for mutations in range(0, numOfMutations):
        ndx = randint(0, len(child)-1)
        child[ndx] = randint(1, maxTake)
    return child

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

def geneticAlgWithSingleMutation(winHistory, counter, mutationRate, maxTake):
    combos = len(winHistory)//2
    pathOptions = []
    counter += 1
    for i in range(0, combos):
        child1 = winHistory[i]
        i += 1
        child2 = winHistory[i]
        child1Beg = child1[:len(child1)//2]
        child1End = child1[len(child1)//2:]
        child2Beg = child2[:len(child2)//2]
        child2End = child2[len(child2)//2:]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        mutate1 = randint(0, 100)
        if mutate1 < mutationRate:
            newChild1 = mutate(newChild1, 1, maxTake)
        mutate2 = randint(0, 100)
        if mutate2 < mutationRate:
            newChild2 = mutate(newChild2, 1, maxTake)
        pathOptions.append(newChild1)
        pathOptions.append(newChild2)
    return pathOptions, counter

def geneticAlgWithMultipleMutations(winHistory, counter, mutationRate, mutationCount, maxTake):
    combos = len(winHistory)//2
    pathOptions = []
    counter += 1
    for i in range(0, combos):
        child1 = winHistory[i]
        i += 1
        child2 = winHistory[i]
        child1Beg = child1[:len(child1)//2]
        child1End = child1[len(child1)//2:]
        child2Beg = child2[:len(child2)//2]
        child2End = child2[len(child2)//2:]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        pathOptions.append(newChild1)
        pathOptions.append(newChild2)
    return pathOptions, counter

def battle(pathOptions, totalPebbles, maxTake, playerFunk):
    wins = 0
    for i in range(0, len(pathOptions)):
        winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i], playerFunk)
        pullPattern = pullPattern[:totalPebbles]
        if winner == 0:
            wins += 1
    return wins

def main():
    totalPebbles = 97
    maxTake = 4
    generationSize = 1000
    reproductionRate = .2
    generations = 0
    winHistory = []
    loseHistory = []
    trainingPlayer = playerRandom
    battlePlayer = playerBest
    desiredWinRate = .65
    for i in range(0, generationSize):
        # Need to give nim a random array that guarantees all the pebbles get taken
        # An array with totalPebbles / 2 elements should guarantee this.
        baseline = [randint(1, maxTake) for x in range(totalPebbles//2)]
        #winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline, trainingPlayer)
        winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline, trainingPlayer)
        pullPattern = pullPattern[:totalPebbles]
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
        # Calculate the number of replacements to generate
        numKids = min([len(winHistory), floor(len(loseHistory)*reproductionRate)])
        numKids = (numKids // 2) * 2
        # With no mutations
        pathOptions, generations = geneticAlg(winHistory, loseHistory, numKids, generations)
        # With a chance at a single mutation per combination
        #pathOptions, generations = geneticAlgWithSingleMutation(winHistory, loseHistory, numKids, generations, 100, maxTake)
        #print('pathOptions: {0}'.format(pathOptions))
        # Clear the histories
        winHistory = []
        loseHistory = []
        # For each of the products of this round of evolution...
        for i in range(0, len(pathOptions)):
            # Have them play again
            #winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i], trainingPlayer)
            winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i], trainingPlayer)
            pullPattern = pullPattern[:totalPebbles]
            # If player 0 wins, add them to the new win history list
            if winner == 0:
                #print('A winning strategy: {0}'.format(pathOptions[i]))
                winHistory.append(pathOptions[i][0:iterations])
            else: 
                loseHistory.append(pathOptions[i][0:iterations])
        print("Number of generated wins out of {0}: {1}".format(len(pathOptions), len(winHistory)))
        # recalculate the winning percentage
        winPercent = len(winHistory) / len(pathOptions)

    wins = battle(pathOptions, totalPebbles, maxTake, battlePlayer)
    print("Number of battle wins out of {0} against playerBest: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, maxTake, playerMax)
    print("Number of battle wins out of {0} against playerMax: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, maxTake, player3)
    print("Number of battle wins out of {0} against player3: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, maxTake, player2)
    print("Number of battle wins out of {0} against player2: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, maxTake, player1)
    print("Number of battle wins out of {0} against player1: {1}".format(generationSize, wins))
    wins = battle(pathOptions, totalPebbles, maxTake, playerRandom)
    print("Number of battle wins out of {0} against playerRandom: {1}".format(generationSize, wins))

main()
