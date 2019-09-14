'''
Created on 11.09.2019

@author: TKler
'''
# Imports und so
import numpy as np
from scipy.stats import logistic
from NetworkTemplate import NetworkTemplate
import random
from builtins import staticmethod


class NIPSNetwork(NetworkTemplate):
    number_of_sensory_inputs = 16
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 4
    number_of_output_units = 22
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)

    def getInput(self):
        input_pattern = self.getInputFromSimplePattern() 

        input_matrix = np.append(input_pattern, self.input_during_run)
        
        return input_matrix

    def applySigmoidFunction(self, matrix):
        return logistic.cdf(matrix)
    
    def takeInputFromSim(self, data):
        self.input_during_run = data
    
    @staticmethod
    def getNumberOfWeights(self):
        return NIPSNetwork.number_of_weights
    
    @staticmethod
    def generateRandomWeights():
        weights = []
        for _i in range(0, NIPSNetwork.number_of_weights):
            weights.append(random.uniform(0, 1))
            
        return weights

