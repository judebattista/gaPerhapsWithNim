from random import randint
#heuristic 1
 
#heuristic 2

def nim(totalPebbles, maxTake, pathOptions):
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
        #num1 = player1()
        num1 = playerRandom(maxTake)
        pullPattern += ('1'*num1)
        i += num1
    return 1, pullPattern, iterations
    

def playerRandom(maxTake):
    num0 = randint(1, maxTake)
    return num0

def trainedPlayer():
    pass

def player1():
    return 4

def baseline():
    counter = 0
    num = randint(0, maxTake)
    player0.append(num)
    counter += num
    num1 = randint(0, maxTake)
    player1.append(num1)
    counter += num1 

def mutate(child, numOfMutations, maxTake):
    for mutations in range(0, numOfMutations):
        ndx = randint(0, len(child)-1)
        child[ndx] = randint(1, maxTake)
    return child

def geneticAlg(winHistory, counter):
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

def main():
    totalPebbles = 97
    maxTake = 4
    generationSize = 1000
    generations = 0
    winHistory = []
    for i in range(0, generationSize):
        # Need to give nim a random array that guarantees all the pebbles get taken
        # An array with totalPebbles / 2 elements should guarantee this.
        baseline = [randint(1, maxTake) for x in range(totalPebbles//2)]
        winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline)
        pullPattern = pullPattern[:totalPebbles]
        if winner == 0:
            print('Winning baseline: {0}'.format(baseline[0:iterations]))
            winHistory.append(baseline[0:iterations])
        else:
            print('Losing baseline: {0}'.format(baseline[0:iterations]))
    print("Number baseline wins out of {0}: {1}".format(generationSize, len(winHistory)))
    winPercent = len(winHistory) / generationSize
    # Until our family gets strong enough...
    while winPercent < .75:
        # Feed the winning paths back into evolution
        # With no mutations
        # pathOptions, generations = geneticAlg(winHistory, generations)
        # With a chance at a single mutation per combination
        pathOptions, generations = geneticAlgWithSingleMutation(winHistory, generations, 100, maxTake)
        #print('pathOptions: {0}'.format(pathOptions))
        # Clear the history
        winHistory = []
        # For each of the products of this round of evolution...
        for i in range(0, len(pathOptions)):
            # Have them play again
            winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i])
            pullPattern = pullPattern[:totalPebbles]
            # If player 0 wins, add them to the new win history list
            if winner == 0:
                print('A winning strategy: {0}'.format(pathOptions[i]))
                winHistory.append(pathOptions[i][0:iterations])
        print("Number of generated wins out of {0}: {1}".format(len(pathOptions), len(winHistory)))
        # recalculate the winning percentage
        winPercent = len(winHistory) / len(pathOptions)

main()
