'''
Created on 23.09.2019

@author: TKler
'''

from NIPSChallenge.NIPSNetwork import NIPSNetwork
import numpy as np
import matplotlib.pyplot as plt
import SafeData

nw = NIPSNetwork(NIPSNetwork.generateRandomWeights())


def weightsPerInput(nw):
    number_of_input = nw.number_of_input_units
    weights_from_input = nw.input_to_hidden_all
    for i in range(0, number_of_input):
        array = np.array(weights_from_input[i])
        array = np.absolute(array)
        mean = np.mean(array)
        print("Input", i, "mean:", mean)
        print(array)

# weightsPerInput(nw)


def hiddenWeights(nw):
    # no_hiddens = 11
    print("Hidden weights", nw.hidden_to_hidden)

# hiddenWeights(nw)


def getOutputData(nw):
    no_outputs = 11
    no_iters = 200
    y = [[0 for _x in range(no_iters)] for _y in range(no_outputs)]
    x = []
    for i in range(0, no_iters):
        array = nw.computeOneStep()
        x.append(i)
        for index in range(0, no_outputs):
            y[index][i] = array[0][index]
    
    for i in range(0, no_outputs):
        plt.plot(x, y[i])
    
    plt.show()

# getOutputData(nw)


def getHiddenLayerOutput(nw):
    no_hiddens = 11
    no_iters = 200
    y = [[0 for _x in range(no_iters)] for _y in range(no_hiddens)]
    x = []
    for i in range(0, no_iters):
        _array = nw.computeOneStep()
        array = nw.last_output_hidden
        x.append(i)
        for index in range(0, no_hiddens):
            y[index][i] = array[0][index]
    
    for i in range(0, no_hiddens):
        plt.plot(x, y[i])
    
    plt.show()


# getHiddenLayerOutput(nw)
pop = SafeData.loadPopulation()
nw = pop[0].nw1
hiddenWeights(nw)
weightsPerInput(nw)
getHiddenLayerOutput(nw)
# getOutputData(nw)

