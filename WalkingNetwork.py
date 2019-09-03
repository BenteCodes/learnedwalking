# Imports und so
import numpy as np
from scipy.stats import logistic
import random
from SimplePatternGenerator import SimplePatternGenerator

# class for that network
# parameters: weights
class WalkingNetwork:
    
    number_of_input_units = 10 #min 4
    number_of_hidden_units = 4
    number_of_output_units = 20
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    number_of_basic_pattern = 4

    # @input weights weights of the network

    def __init__(self, weights): 
        self.checkParameter(weights)    
        self.initNetwork(weights)
        self.initInputPattern()

    
    def checkParameters(self, weights):
        if not(len(weights) == self.number_of_weights):
            print("Paramcheck: Weights of incorrect number_of_weights")
        
            
    # disects the weights into the corresponding network parts 
    # 10input -> 4 hidden with recurrant -> 20 output   
    def initNetwork(self, weights):
        self.last_state_hidden = np.ones((1, self.number_of_hidden_units)) #last states values need to be known for the algo and are 1 at the first run.
        
        position_start = 0
        position_end = self.number_of_input_units * self.number_of_hidden_units
        self.input_to_hidden_all = np.matrix(weights[position_start:position_end])
        self.input_to_hidden_all = np.reshape(self.hidden_to_output_all, (self.number_of_input_units, self.number_of_hidden_units))

        position_start = position_end
        position_end += self.number_of_hidden_units        
        self.hidden_to_hidden = np.matrix(weights[position_start:position_end])

        position_start = position_end
        position_end += (self.number_of_hidden_units * self.number_of_output_units)         
        self.hidden_to_output_all = np.matrix(weights[position_start:position_end])
        self.hidden_to_output_all = np.reshape(self.hidden_to_output_all, (self.number_of_hidden_units, self.number_of_output_units)) #sort after connection not just a long list
    
    def initInputPattern(self):
        self.simple_pattern = SimplePatternGenerator('sinepattern.csv', 'plussinepattern.csv', 'blopppattern.csv', 'broadsinepattern.csv')    
    
    # need to be a 10x1 matrix for matrix purposes, though only 5 get used
    def getInput(self):
        input_matrix = np.zeros((self.number_of_input_units, 1))

        input_matrix = self.getInputFromSimplePattern(input_matrix, np)

        return input_matrix

    
    def getInputFromSimplePattern(self, input_matrix, np):
        self.simple_pattern.nextStep()
        
        for index in range(self.number_of_basic_pattern):
            np.put(input_matrix, index, self.simple_pattern[index])
        
        return input_matrix


    # forewardpropagation
    # input is a np matrix [10x1]
    def computeOneStep(self):
        state_input = self.getInput()
        hidden = self.number_of_hidden_units
        while hidden > 1:
            state_input = np.concatenate((state_input, self.input_matrix), axis=1)
            hidden -=  1

        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        #done until here
        assembled_hidden_weights = self.input_to_hidden_all
        assembled_hidden_weights = np.insert(assembled_hidden_weights, [self.number_of_input_units], np.transpose(self.hidden_to_hidden), axis=1)
        state_hidden = (logistic.cdf(np.matrix([np.diagonal(assembled_hidden_weights * assembled_hidden_input, 0)]))+2)-1 # TODO check this please, wtf + names!!

        #print(state_hidden)
        state_output = (logistic.cdf(state_hidden * self.hidden_to_output_all) * 2) - 1
        #print(state_output)
        self.last_state_hidden = state_hidden

        self.areThereNonZeroOutputs = self.areThereNonZeroOutputs(state_output)
        
        return state_output

    def areThereNonZeroOutputs(self, state_output):
        return abs(max(state_output, key=abs)) > 0.05

    def resetHiddenLayer(self):
        self.last_state_hidden = np.ones((1, 4))
    
    def getNumberOfWeights(self):
        return self.number_of_weights
    
    def getWeightAt(self, index):
        return self.weight[index]
    
    def getMovement(self):
        return self.areThereNonZeroOutputs
    
    @staticmethod
    def createRandomNetwork():
        weights = []
        for _i in range(0, WalkingNetwork.number_of_weights):
            weights.append(random.uniform(-1, 1))
            
        return WalkingNetwork(weights)
