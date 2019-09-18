import numpy as np
from SimplePatternGenerator import SimplePatternGenerator
from Network3LayerAbstract import Network3LayerAbstract
from abc import abstractmethod
import random


class NetworkTemplate(Network3LayerAbstract):

    def __init__(self, weights): 
        self.checkParameters(weights)    
        self.initNetwork(weights)
        self.initInputPattern()
    
    def checkParameters(self, weights):
        if not(len(weights) == self.number_of_weights):
            print("Paramcheck: Weights of incorrect number_of_weights")

    def initInputPattern(self):
        self.simple_pattern = SimplePatternGenerator()    
    
    '''
    Combines the weights from the input layer to the hidden layer and the recurrent weights of the hidden layer
    into one matrix.
    Only needed once per network
    ''' 
    
    def getInputFromSimplePattern(self):
        return self.simple_pattern.nextStep()

    def computeHiddenOutputs(self):
        nw_input = np.array([self.getInputFromSimplePattern()])
        value_hidden_neurons = np.matmul(nw_input, self.input_to_hidden_all)
        for index in range(0, self.number_of_hidden_units):
            value_hidden_neurons[0][index] += self.hidden_to_hidden[0][index] * self.last_output_hidden[0][index]
        
        value_hidden_neurons = self.normaliseNeuronInputSomewhat(value_hidden_neurons)
        self.last_output_hidden = self.applyActivationFunction(value_hidden_neurons)

    def computeOutputsFromHiddenOnwards(self):
        value_output_neurons = np.matmul(self.last_output_hidden, self.hidden_to_output_all) 
        value_output_neurons = self.normaliseNeuronInputSomewhat(value_output_neurons) 
        network_output = self.applyActivationFunction(value_output_neurons)
        return network_output

    '''
    One run through the network. From input to hidden, hidden to output
    With recursive neurons and sigmoid function
    '''

    def computeOneStep(self):
        self.computeHiddenOutputs()
        
        return self.computeOutputsFromHiddenOnwards()
    
    def normaliseNeuronInputSomewhat(self, values):
        return np.divide(values, len(values[0]) / 2)

    def resetHiddenLayer(self):
        self.last_output_hidden = np.ones((1, self.number_of_hidden_units))  # set to neutral element
    
    def getWeightAt(self, index):
        return self.weights[index]
    
    @classmethod
    def getNumberOfWeights(cls):
        return cls.number_of_weights
        
    @classmethod
    def generateRandomWeights(cls):
        weights = []
        for _i in range(0, cls.number_of_weights):
            weights.append(random.uniform(cls.start_weights[0], cls.start_weights[1]))
            
        return weights

    @abstractmethod
    def applyActivationFunction(self, matrix):
        return NotImplementedError

    @abstractmethod
    def getInput(self):
        return NotImplementedError
    
    @abstractmethod
    def takeInputFromSim(self, data):
        return NotImplementedError
