from random import randint, sample, uniform
from math import floor, ceil

def nim(totalPebbles, maxTake, pathOptions, playerFunk):
    pullPattern = ""
    iterations = 0
    i = 0
    choiceNdx = 0
    while i < totalPebbles:
        iterations += 1
        num0 = pathOptions[choiceNdx]
        #print('num0 = {0}'.format(num0))
        #pullPattern += ('0'*num0)
        i += num0
        if i >= totalPebbles:
            return 0, pullPattern, iterations
        num1 = playerFunk(maxTake, i)
        #pullPattern += ('1'*num1)
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

def playerGenerous(maxTake, i):
    choice = (i % maxTake) - 1
    if choice <= 0:
        return maxTake + choice
    return choice

def mutateChild(child, numOfMutations, maxTake):
    for mutations in range(0, numOfMutations+1):
        ndx = randint(0, len(child)-1)
        child[ndx] = randint(1, maxTake)
    return child

def mutateGene(child, mutationRate, maxTake):
    chancePerGene = mutationRate / len(child)
    for ndx, gene in enumerate(child):
        if (uniform(0.0, 1.0) < chancePerGene):
            child[ndx] = randint(1, maxTake)
    return child

def geneticAlg(winHistory, loseHistory, numKids, counter, maxTake):
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

def geneticAlgWithSingleMutation(winHistory, loseHistory, numKids, mutationRate, counter, maxTake):
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
            print("mutation child1 Single")
            newChild1 = mutateChild(newChild1, 1, maxTake)
        mutate2 = randint(0, 100)
        if mutate2 < mutationRate:
            print("mutation child2 Single")
            newChild2 = mutateChild(newChild2, 1, maxTake)

        # Replacement
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild1
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild2
    # Combine the winners with the evolved population
    pathOptions = winHistory + loseHistory
    return pathOptions, counter

def geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, mutationRate, counter, maxTake):
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
        mutateGene(newChild1, mutationRate, maxTake)
        mutateGene(newChild2, mutationRate, maxTake)

        # Replacement
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild1
        ndx = kidIndices.pop()
        loseHistory[ndx] = newChild2
    # Combine the winners with the evolved population
    pathOptions = winHistory + loseHistory
    return pathOptions, counter


def battle(pathOptions, totalPebbles, maxTake, playerFunk):
    wins = 0
    for i in range(0, len(pathOptions)):
        winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i], playerFunk)
        pullPattern = pullPattern[:totalPebbles]
        if winner == 0:
            wins += 1
    return wins

def playHuman(totalPebbles, maxTake, choices):
    move = 0
    maxMoves = len(choices)
    remainingPebbles = totalPebbles
    while(remainingPebbles > 0):
        remainingPebbles -= choices[move]
        if remainingPebbles <= 0:
            print('Joshua takes {0} pebbles. 0 remaining.'.format(choices[move]))
            return 0
        else:
            print('Joshua takes {0} pebbles. {1} remaining'.format(choices[move], remainingPebbles))
            move += 1
            move = move % maxMoves
        playerTake = int(input('How many pebbles would you like to take? '))
        if playerTake > maxTake:
            playerTake = maxTake
        elif playerTake < 1:
            playerTake = 1
        remainingPebbles -= playerTake
        if remainingPebbles <= 0:
            print('You take {0}, leaving 0 remaining'.format(playerTake))
            return 1
        else:
            print('You take {0}, leaving {1} remaining'.format(playerTake, remainingPebbles))
        

def menu():
    sep = '#'*100
    operations = [
        'U.S. First Strike',
        'U.S.S.R. First Strike',
        'NATO / Warsaw Pact',
        'Far East Strategy',
        'U.S. / U.S.S.R. escalation',
        'Middle East War',
        'U.S.S.R. / China Attack',
        'India / Pakistan War',
        'Mediterranean War',
        'Hong Kong Variant',
        'SEATO Decapitating',
        'Cuban Provocation',
        'Inadvertent',
        'Atlantic Heavy',
        'Cuban Paramilitary',
        'Nicaraguan Pre-emptive',
        'Pacific Territorial',
        'Burmese Theaterwide',
        'Turkish Decoy',
        'Argentina Escalation',
        'Iceland Maximum',
        'Arabian Theaterwide',
        'U.S. Subversion',
        'Australian Maneuver',
        'Sudan Surprise',
        'NATO Territorial',
        'Zaire Alliance',
        'Iceland Incident',
        'English Escalation',
        'Zaire Screen',
        'Middle East Heavy',
        'Mexican Takeover',
        'Chad Alert',
        'Saudi Maneuver',
        'African Territorial',
        'Ethiopian Calamity',
        'Turkish Heavy',
        'NATO Incursion',
        'U.S. Defense',
        'Cambodian Heavy',
        '(Warsaw) Pact Medium',
        'Arctic Minimal',
        'Mexican Domestic',
        'Taiwanese Theaterwide',
        'Pacific Maneuver',
        'Portugal Revolution',
        'Albanian Decoy',
        'Palestinian Local',
        'Moroccan Minimal',
        'Czech Option',
        'French Alliance',
        'Arabian Clandestine',
        'Gabon Rebellion',
        'Northern Maximum',
        'SEATO Takeover',
        'Hawaiian Escalation',
        'Iranian Maneuver',
        'NATO Containment',
        'Swiss Incident',
        'Cuba Minimal',
        'Iceland Escalation',
        'Vietnamese Retaliation',
        'Syrian Provocation',
        'Libyan Local',
        'Gabon Takeover',
        'Romanian War',
        'Middle East Offensive',
        'Denmark Massive',
        'Chile Confrontation',
        'South African Subversion',
        'U.S.S.R. Alert',
        'Nicaraguan Thrust',
        'Greenland Domestic',
        'Iceland Heavy',
        'Kenya Option',
        'Pacific Defense',
        'Uganda Maximum',
        'Thai Subversion',
        'Romanian Strike',
        'Pakistan Sovereignty',
        'Afghan Misdirection',
        'Thai Variation',
        'Northern Territorial',
        'Polish Paramilitary',
        'South African Offensive',
        'Panama Misdirection',
        'Scandinavian Domestic',
        'Jordan Pre-emptive',
        'English Thrust',
        'Burmese Manuever',
        'Spain Counter',
        'Arabian Offensive',
        'Chad Interdiction',
        'Taiwan Misdirection',
        'Bangladesh Theaterwide',
        'Ethiopian Local',
        'Italian Takeover',
        'Vietnamese Incident',
        'English Pre-emptive',
        'Denmark Alternate',
        'Thai Confrontation',
        'Taiwan Surprise',
        'Brazilian Strike',
        'Venezuela Sudden',
        'Malaysian Alert',
        'Israel Discretionary',
        'Libyan Action',
        'Palestinian Tactical',
        'NATO Alternate',
        'Cypress Maneuver',
        'Egypt Misdirection',
        'Bangladesh Thrust',
        'Kenya Defense',
        'Bangladesh Containment',
        'Vietnamese Strike',
        'Albanian Containment',
        'Gabon Surprise',
        'Iraq Sovereignty',
        'Vietnamese Sudden',
        'Lebanon Interdiction',
        'Taiwan Domestic',
        'Algerian Sovereignty',
        'Arabian Strike',
        'Atlantic Sudden',
        'Mongolian Thrust',
        'Polish Decoy',
        'Alaskan Discretionary',
        'Canadian Thrust',
        'Arabian Light',
        'South African Domestic',
        'Tunisian Incident',
        'Malaysian Maneuver',
        'Jamaica Decoy',
        'Malaysian Minimal',
        'Russian Sovereignty',
        'Chad Option',
        'Bangladesh War',
        'Burmese Containment',
        'Asian Theaterwide',
        'Bulgarian Clandestine',
        'Greenland Incursion',
        'Egypt Surgical',
        'Czech Heavy',
        'Taiwan Confrontation',
        'Greenland Maximum',
        'Uganda Offensive',
        'Caspian Defense'
    ]
    print()
    print()
    print()
    print()
    print(sep)
    print('GREETINGS PROFESSOR FALKIN.')
    print('WOULD YOU LIKE TO PLAY A GAME?')
    print('1. Global Thermonuclear War')
    print('2. Nim')
    print(sep)
    print()
    print()
    print()
    print()
    choice = input()
    if choice == '1':
        print('OPERATION\t\t\tWINNER')
        print('='*9 + '\t\t\t' + '='*6)
        for op in operations:
            blocks = len(op) // 8
            distance = 4 - blocks
            space = '\t'*distance
            #print('blocks: {0}, distance: {1}'.format(blocks, distance))
            print('{0}{1}NONE'.format(op.upper(), space))
        print()
        print()
        print()
        print()
        print('A STRANGE GAME.')
        print('THE ONLY WINNING MOVE IS NOT TO PLAY.') 
        print('HOW ABOUT A NICE GAME OF NIM?')
        print()
        print()
        print()
        print()

def main():
    totalPebbles = 97
    maxTake = 4
    generationSize = 1000
    reproductionRate = .5
    mutationRate = 1
    generations = 0
    winHistory = []
    loseHistory = []
    trainingPlayer = playerRandom
    battlePlayer = playerBest
    desiredWinRate = .67
    sep = '#'*100
    for foo in range(20):
        generations = 0
        winPercent = 0
        winHistory = []
        loseHistory = []
        for i in range(0, generationSize):
            # Need to give nim a random array that guarantees all the pebbles get taken
            # An array with totalPebbles / 2 elements should guarantee this.
            baseline = [randint(1, maxTake) for x in range(totalPebbles//2)]
            #winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline, trainingPlayer)
            winner, pullPattern, iterations = nim(totalPebbles, maxTake, baseline, trainingPlayer)
            #pullPattern = pullPattern[:totalPebbles]
            if winner == 0:
                #print('Winning baseline: {0}'.format(baseline[0:iterations]))
                winHistory.append(baseline[0:iterations])
            else:
                #print('Losing baseline: {0}'.format(baseline[0:iterations]))
                loseHistory.append(baseline[0:iterations])
        #print("Number baseline wins out of {0}: {1}".format(generationSize, len(winHistory)))
        winPercent = len(winHistory) / generationSize
        # Until our family gets strong enough...
        while winPercent < desiredWinRate:
            # Feed the winning paths back into evolution
            
            # With no mutations
            # Calculate the number of replacements to generate
            #numKids = min([len(winHistory), floor(len(loseHistory)*reproductionRate)])
            #numKids = (numKids // 2) * 2
            #pathOptions, generations = geneticAlg(winHistory, loseHistory, numKids, generations, maxTake)

            # With multiple mutations - breakpoints
            # #determine amount of mutations/if any
            # if winPercent < (desiredWinRate*.6):
            #     pathOptions, generations = geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, mutationRate, generations, maxTake)
            # elif winPercent < (desiredWinRate*.9):
            #     pathOptions, generations = geneticAlgWithSingleMutation(winHistory, loseHistory, numKids, mutationRate, generations, maxTake)
            # else:
            #     pathOptions, generations = geneticAlg(winHistory, loseHistory, numKids, generations, maxTake)

            # With multiple mutations, continuous mutation scaling
            scalingMutationRate = min([0, 1 - winPercent]) * mutationRate
            #scalingReproductionRate = min([0, 1 - winPercent]) * reproductionRate
            scalingReproductionRate = reproductionRate
            numKids = min([len(winHistory), floor(len(loseHistory)*scalingReproductionRate)])
            numKids = (numKids // 2) * 2
            pathOptions, generations = geneticAlgWithMultipleMutations(winHistory, loseHistory, numKids, scalingMutationRate, generations, maxTake)
            # With a chance at a single mutation per combination
            #pathOptions, generations = geneticAlgWithSingleMutation(winHistory, loseHistory, numKids, generations, 100, maxTake)
            #print('pathOptions: {0}'.format(pathOptions))
            # Clear the histories
            winHistory = []
            loseHistory = []
            # For each of the products of this round of evolution...
            for i in range(0, len(pathOptions)):
                # Have them play again
                winner, pullPattern, iterations = nim(totalPebbles, maxTake, pathOptions[i], trainingPlayer)
                #pullPattern = pullPattern[:totalPebbles]
                # If player 0 wins, add them to the new win history list
                if winner == 0:
                    #print('A winning strategy: {0}'.format(pathOptions[i]))
                    winHistory.append(pathOptions[i][0:iterations])
                else: 
                    loseHistory.append(pathOptions[i][0:iterations])
            #print("Number of generated wins out of {0}: {1}".format(len(pathOptions), len(winHistory)))
            # recalculate the winning percentage
            winPercent = len(winHistory) / len(pathOptions)
            #print('AAA - It took {0} generations to achieve a win rate of at least {1}.'.format(generations, desiredWinRate))
        print('BBB - It took {0} generations to achieve a win rate of at least {1}.'.format(generations, desiredWinRate))
        with open('stats.txt', 'a+') as outfile:
            outfile.write(str(generations) + '\n')
    #print('CCC - It took {0} generations to achieve a win rate of at least {1}.'.format(generations, desiredWinRate))
    # wins = battle(pathOptions, totalPebbles, maxTake, battlePlayer)
    # print("Number of battle wins out of {0} against playerBest: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, playerMax)
    # print("Number of battle wins out of {0} against playerMax: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, player3)
    # print("Number of battle wins out of {0} against player3: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, player2)
    # print("Number of battle wins out of {0} against player2: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, player1)
    # print("Number of battle wins out of {0} against player1: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, playerRandom)
    # print("Number of battle wins out of {0} against playerRandom: {1}".format(generationSize, wins))
    # wins = battle(pathOptions, totalPebbles, maxTake, playerGenerous)
    # print("Number of battle wins out of {0} against playerGenerous: {1}".format(generationSize, wins))
    #menu()
    #strat = pathOptions[randint(0, len(pathOptions) - 1)]
    #winner = playHuman(totalPebbles, maxTake, strat)
    print()
    print()
    print()
    print(sep)
    if winner == 0:
        print('BETTER LUCK NEXT TIME PROFESSOR FALKIN')
    else:
        print('GOOD GAME PROFESSOR FALKIN')
    print(sep)
    print()
    print()
    print()
    
main()
