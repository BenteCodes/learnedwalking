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

    def prepareWeightsToHiddenUnits(self):
        weights_to_hidden_units = np.concatenate((self.input_to_hidden_all, self.hidden_to_hidden), axis=0)
        weights_to_hidden_units = np.transpose(weights_to_hidden_units)
        return weights_to_hidden_units
    
    def getInputFromSimplePattern(self):
        return self.simple_pattern.nextStep()

    '''
    Creates one inputvector for every hidden neuron and saves them into a 
    number_of_input_units X number_of_hidden_units matrix
    '''

    def duplicateInputByNumberOfHiddenUnits(self, state_input):
        state_input = np.array([state_input])
        input_matrix = state_input
        for _i in range(1, self.number_of_hidden_units):
            state_input = np.concatenate((state_input, input_matrix), axis=0)
        return state_input

    '''
    Adds the previous output of the hidden units to the input vectors in the matrix
    '''

    def addRecurrentInputs(self, state_input):
        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        return assembled_hidden_input

    '''
    Fetches all input values and creates the matrix for the multiplication
    '''

    def createHiddenLayerInput(self):
        oneD_input_vector = self.getInput()
        number_of_input_units_times_number_of_hidden_units_matrix = self.duplicateInputByNumberOfHiddenUnits(oneD_input_vector)
        values_into_hidden_units = self.addRecurrentInputs(number_of_input_units_times_number_of_hidden_units_matrix)
        return values_into_hidden_units

    '''
    Applies the sigmoid function to all values in the matrix.
    Afterwards streches and offsets the values so we get values between -1 and 1 instead of 0 and 1
    '''

    '''
    One run through the network. From input to hidden, hidden to output
    With recursive neurons and sigmoid function
    '''

    def computeOneStep(self):
        hidden_layer_input = self.createHiddenLayerInput()
        
        # Actual computation of the output of the hidden layer
        # returns a 1 X number_of_hidden_units matrix
        diagonal_of_matrix_mul = np.matrix([np.diagonal(self.weights_to_hidden_units * hidden_layer_input, 0)])
        diagonal_of_matrix_mul = self.normaliseNeuronInputSomewhat(diagonal_of_matrix_mul)
        self.last_state_hidden = self.applyActivationFunction(diagonal_of_matrix_mul)
        
        # Actual computation of the output of the network
        # returns a number_of_output_units X 1 matrixs
        matrix_mul = self.last_state_hidden * self.hidden_to_output_all
        matrix_mul = self.normaliseNeuronInputSomewhat(matrix_mul)
        network_output = self.applyActivationFunction(matrix_mul)

        return network_output
    
    def normaliseNeuronInputSomewhat(self, values):
        return np.divide(values, len(values) / 2)

    def resetHiddenLayer(self):
        self.last_state_hidden = np.ones((1, self.number_of_hidden_units))  # set to neutral element
    
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
