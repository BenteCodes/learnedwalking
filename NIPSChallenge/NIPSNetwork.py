'''
Created on 11.09.2019

@author: TKler
'''
# Imports und so
import numpy as np
from scipy.stats import logistic
from MA.SimplePatternGenerator import SimplePatternGenerator
from Network3LayerAbstract import Network3LayerAbstract
import random
from builtins import staticmethod


class NIPSNetwork(Network3LayerAbstract):
    number_of_sensory_inputs = 16
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs  # TODO split into sensory and pattern input # min 4
    number_of_hidden_units = 4
    number_of_output_units = 22
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)

    # @input_during_run weights weights of the network

    def __init__(self, weights): 
        self.checkParameters(weights)    
        self.initNetwork(weights)
        self.initInputPattern()
        self.are_there_non_zero_outputs_value = False
    
    def checkParameters(self, weights):
        if not(len(weights) == self.number_of_weights):
            print("Paramcheck: Weights of incorrect number_of_weights")
    
    def initInputPattern(self):
        self.simple_pattern = SimplePatternGenerator()    
    
    '''
    Combines the weights from the input_during_run layer to the hidden layer and the recurrent weights of the hidden layer
    into one matrix.
    Only needed once per network
    ''' 

    def prepareWeightsToHiddenUnits(self):
        weights_to_hidden_units = np.concatenate((self.input_to_hidden_all, self.hidden_to_hidden), axis=0)
        weights_to_hidden_units = np.transpose(weights_to_hidden_units)
        return weights_to_hidden_units
    
    def getInput(self):

        input_pattern = self.getInputFromSimplePattern() 

        input_matrix = np.append(input_pattern, self.input_during_run)
        
        return input_matrix
    
    def getInputFromSimplePattern(self):
        results = self.simple_pattern.nextStep()
        
        return np.array(results)

    # forewardpropagation
    # input_during_run is a np matrix [10x1]

    '''
    Creates one inputvector for every hidden neuron and saves them into a 
    number_of_input_units X number_of_hidden_units matrix
    '''

    def duplicateInputByNumberOfHiddenUnits(self, state_input):
        hidden = self.number_of_hidden_units
        input_matrix = state_input
        while hidden > 1:
            state_input = np.concatenate((state_input, input_matrix), axis=1)
            hidden -= 1
        return state_input

    '''
    Adds the previous output of the hidden units to the input_during_run vectors in the matrix
    '''

    def addRecurrentInputs(self, state_input):
        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        return assembled_hidden_input

    def appendHiddenLayer(self, oneD_input_vector):
        number_of_input_units_times_number_of_hidden_units_matrix = self.duplicateInputByNumberOfHiddenUnits(oneD_input_vector)
        values_into_hidden_units = self.addRecurrentInputs(number_of_input_units_times_number_of_hidden_units_matrix)
        return values_into_hidden_units

    def createHiddenLayerInput(self):
        oneD_input_vector = self.getInput()
        values_into_hidden_units = self.appendHiddenLayer(oneD_input_vector)
        return values_into_hidden_units

    '''
    Applies the sigmoid function to all values in the matrix.
    Afterwards streches and offsets the values so we get values between -1 and 1 instead of 0 and 1
    '''

    def applySigmoidFunction(self, matrix):
        return logistic.cdf(matrix)

    '''
    One run through the network. From input_during_run to hidden, hidden to output
    With recursive neurons and sigmoid function
    '''

    def computeOneStep(self):
        hidden_layer_input = self.createHiddenLayerInput()
        
        # Actual computation of the output of the hidden layer
        # returns a 1 X number_of_hidden_units matrix
        diagonal_of_matrix_mul = np.matrix([np.diagonal(self.weights_to_hidden_units * hidden_layer_input, 0)])
        diagonal_of_matrix_mul = self.ropValues(diagonal_of_matrix_mul)
        self.last_state_hidden = self.applySigmoidFunction(diagonal_of_matrix_mul)
        
        # Actual computation of the output of the network
        # returns a number_of_output_units X 1 matrixs
        matrix_mul = self.last_state_hidden * self.hidden_to_output_all
        matrix_mul = self.ropValues(matrix_mul)
        network_output = self.applySigmoidFunction(matrix_mul)

        return network_output
    
    def cropValues(self, values):
        return np.divide(values, len(values) / 2)

    def resetHiddenLayer(self):
        self.last_state_hidden = np.ones((1, self.number_of_hidden_units))  # set to neutral element
    
    def takeInputFromSim(self, data):
        self.input_during_run = data
    
    @staticmethod
    def getNumberOfWeights(self):
        return NIPSNetwork.number_of_weights
    
    def getWeightAt(self, index):
        return self.weights[index]

    @staticmethod
    def generateRandomWeights():
        weights = []
        for _i in range(0, NIPSNetwork.number_of_weights):
            weights.append(random.uniform(0, 1))
            
        return weights

