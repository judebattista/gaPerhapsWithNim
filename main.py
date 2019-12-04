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
        pullPattern += ('0'*num0)
        i += num0
        if i >= totalPebbles:
            return 0, pullPattern
        num1 = player1()
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

def geneticAlg(winHistory, counter):
    combos = len(winHistory)//2
    pathOptions = []
    counter += 1
    for i in range(0, combos):
        child1 = winHistory[i]
        i += 1
        child2 = winHistory[i]
        child1Beg = child1[:len(child1//2)]
        child1End = child1[len(child1//2):]
        child2Beg = child2[:len(child2//2)]
        child2End = child2[len(child2//2):]
        newChild1 = child1Beg + child2End
        newChild2 = child2Beg + child1End
        pathOptions.append(newChild1)
        pathOptions.append(newChild2)
    return pathOptions, counter

def main():
    totalPebbles = 97
    maxTake = 4
    generationSize = 100
    counter = 0
    winHistory = []
    for i in range(0, generationSize):
        # Need to give nim a random array that guarantees all the pebbles get taken
        # An array with totalPebbles / 2 elements should guarantee this.
        baseline = [randint(1, maxTake) for x in range(totalPebbles//2)]
        winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline)
        pullPattern = pullPattern[:totalPebbles]
        if winner == 0:
            winHistory.append(baseline[0:iterations])
    print("Number baseline wins out of {0}: {1}".format(generationSize, len(winHistory)))
    while len(winHistory) < 65:
        pathOptions, counter = geneticAlg(winHistory, counter)

main()
