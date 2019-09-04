# Imports und so
import numpy as np
from scipy.stats import logistic
import random
from SimplePatternGenerator import SimplePatternGenerator


# class for that network
# parameters: weights
class Network:
    
    number_of_input_units = 10  # min 4
    number_of_hidden_units = 4
    number_of_output_units = 20
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)

    # @input weights weights of the network

    def __init__(self, weights): 
        self.checkParameters(weights)    
        self.initNetwork(weights)
        self.initInputPattern()
        self.are_there_non_zero_outputs_value = False
    
    def checkParameters(self, weights):
        if not(len(weights) == self.number_of_weights):
            print("Paramcheck: Weights of incorrect number_of_weights")
            
    # disects the weights into the corresponding network parts 
    # 10input -> 4 hidden with recurrant -> 20 output   
    def initNetwork(self, weights):
        self.last_state_hidden = np.ones((1, self.number_of_hidden_units))  # last states values need to be known for the algo and are 1 at the first run.
        
        position_start = 0
        position_end = self.number_of_input_units * self.number_of_hidden_units
        self.input_to_hidden_all = np.matrix(weights[position_start:position_end])
        self.input_to_hidden_all = np.reshape(self.input_to_hidden_all, (self.number_of_input_units, self.number_of_hidden_units))

        position_start = position_end
        position_end += self.number_of_hidden_units        
        self.hidden_to_hidden = np.matrix(weights[position_start:position_end])
        
        self.weights_to_hidden_units = self.prepareWeightsToHiddenUnits()

        position_start = position_end
        position_end += (self.number_of_hidden_units * self.number_of_output_units)         
        self.hidden_to_output_all = np.matrix(weights[position_start:position_end])
        self.hidden_to_output_all = np.reshape(self.hidden_to_output_all, (self.number_of_hidden_units, self.number_of_output_units))  # sort after connection not just a long list
    
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
    
    # need to be a 10x1 matrix for matrix purposes, though only 5 get used
    def getInput(self):
        input_matrix = np.zeros((self.number_of_input_units, 1))

        input_matrix = self.getInputFromSimplePattern(input_matrix, np)

        return input_matrix
    
    def getInputFromSimplePattern(self, input_matrix, np):
        results = self.simple_pattern.nextStep()
        
        for index in range(self.simple_pattern.getNumberOfPatterns()):
            np.put(input_matrix, index, results[index])
        
        return input_matrix

    # forewardpropagation
    # input is a np matrix [10x1]

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
    Adds the previous output of the hidden units to the input vectors in the matrix
    '''

    def addRecurrentInputs(self, state_input):
        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        return assembled_hidden_input

    '''
    Fetches all input values and creates the matrix for the multiplication
    '''

    def createInputValueMatrix(self):
        oneD_input_vector = self.getInput()
        number_of_input_units_times_number_of_hidden_units_matrix = self.duplicateInputByNumberOfHiddenUnits(oneD_input_vector)
        values_into_hidden_units = self.addRecurrentInputs(number_of_input_units_times_number_of_hidden_units_matrix)
        return values_into_hidden_units

    def computeOneStep(self):
        values_into_hidden_units = self.createInputValueMatrix()
        
        # Actual computation of the output of the hidden layer
        # returns a number_of_hidden_units vector and saves it
        state_hidden = (logistic.cdf(np.matrix([np.diagonal(self.weights_to_hidden_units * values_into_hidden_units, 0)])) + 2) - 1  # TODO check this please, wtf + names!!
        self.last_state_hidden = state_hidden
        
        # Actual computation of the output of the network
        # returns a number_of_output_units vector
        state_output = (logistic.cdf(state_hidden * self.hidden_to_output_all) * 2) - 1

        self.areThereNonZeroOutputs(list(state_output))
        return state_output

    def areThereNonZeroOutputs(self, state_output):
        are_there_non_zero_outputs_array = abs(max(state_output, key=abs)) > 0.05
        self.are_there_non_zero_outputs_value = (True in are_there_non_zero_outputs_array) == True
    
    def resetHiddenLayer(self):
        self.last_state_hidden = np.ones((1, 4))
    
    def getNumberOfWeights(self):
        return self.number_of_weights
    
    def getWeightAt(self, index):
        return self.weight[index]
    
    def getMovement(self):
        return self.are_there_non_zero_outputs_value
    
    @staticmethod
    def generateRandomWeights():
        weights = []
        for _i in range(0, Network.number_of_weights):
            weights.append(random.uniform(-1, 1))
            
        return weights

