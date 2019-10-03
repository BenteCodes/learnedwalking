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

    def initNetwork(self, weights):
        self.weights = weights
        self.last_output_hidden = []
        self.resetHiddenLayer() 
        
        position_start = 0
        position_end = self.number_of_input_units * self.number_of_hidden_units
        self.input_to_hidden_all = np.array([weights[position_start:position_end]])
        self.input_to_hidden_all = np.reshape(self.input_to_hidden_all, (self.number_of_input_units, self.number_of_hidden_units))

        position_start = position_end
        position_end += self.number_of_hidden_units        
        self.hidden_to_hidden = np.array([weights[position_start:position_end]])

        position_start = position_end
        position_end += (self.number_of_hidden_units * self.number_of_output_units)         
        self.hidden_to_output_all = np.array([weights[position_start:position_end]])
        self.hidden_to_output_all = np.reshape(self.hidden_to_output_all, (self.number_of_hidden_units, self.number_of_output_units))  # sort after connection not just a long list

        position_start = position_end
        position_end += (self.number_of_input_units * self.number_of_output_units)
        self.input_to_output_all = np.array([weights[position_start:position_end]])
        self.input_to_output_all = np.reshape(self.input_to_output_all, (self.number_of_input_units, self.number_of_output_units))  # sort after connection not just a long list
        
    def initInputPattern(self):
        self.simple_pattern = SimplePatternGenerator()    
    
    '''
    Combines the weights from the input layer to the hidden layer and the recurrent weights of the hidden layer
    into one matrix.
    Only needed once per network
    ''' 
    
    def getInputFromSimplePattern(self):
        return self.simple_pattern.nextStep()

    def computeHiddenOutputs(self, nw_input, input_to_hidden_all, last_output_hidden, hidden_to_hidden):
        value_hidden_neurons = np.matmul(nw_input, input_to_hidden_all)
        for index in range(0, self.number_of_hidden_units):  # append the hidden layer inputs. this has to be done one by one, as they are not fully connected, but just one weight per line
            value_hidden_neurons[0][index] += hidden_to_hidden[0][index] * last_output_hidden[0][index]
        
        value_hidden_neurons = self.normaliseNeuronInputSomewhat(value_hidden_neurons, self.number_of_input_units + 1)
        value_hidden_neurons = (self.applyActivationFunction(value_hidden_neurons))  # TODO monitor this
        
        return value_hidden_neurons

    def computeOutputsFromHiddenOnwards(self, last_output_hidden, hidden_to_output_all, nw_input, input_to_output_all):
        value_output_neurons1 = np.matmul(last_output_hidden, hidden_to_output_all) 
        value_output_neurons1 = self.normaliseNeuronInputSomewhat(value_output_neurons1, self.number_of_hidden_units) 
        
        value_output_neurons2 = np.matmul(nw_input, input_to_output_all)
        value_output_neurons2 = self.normaliseNeuronInputSomewhat(value_output_neurons2, self.number_of_input_units) 
        
        network_output = self.applyActivationFunction(value_output_neurons1 + value_output_neurons2)
        return network_output

    '''
    One run through the network. From input to hidden, hidden to output
    With recursive neurons and sigmoid function
    '''

    def computeOneStep(self):
        nw_input = np.array([self.getInputFromSimplePattern()])
        self.last_output_hidden = self.computeHiddenOutputs(nw_input, self.input_to_hidden_all, self.last_output_hidden, self.hidden_to_hidden)
        
        return self.computeOutputsFromHiddenOnwards(self.last_output_hidden, self.hidden_to_output_all, nw_input, self.input_to_output_all)
    
    def normaliseNeuronInputSomewhat(self, values, no_inputs):
        return np.divide(values, no_inputs / 2)

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
            weights.append(random.uniform(cls.start_weights_range[0], cls.start_weights_range[1]))
            
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
