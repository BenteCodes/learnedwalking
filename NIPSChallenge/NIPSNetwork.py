'''
Created on 11.09.2019

@author: TKler
'''
import numpy as np
from scipy.stats import logistic
from NetworkTemplate import NetworkTemplate


class NIPSNetwork(NetworkTemplate):
    
    number_of_sensory_inputs = 16
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 4
    number_of_output_units = 22
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    start_weights = [0, 1]
    
    def getInput(self):
        input_pattern = self.getInputFromSimplePattern() 
        self.input_during_run = np.zeros((16, 1))  # TODO This has to be initialized and implemented for usefull data
        input_matrix = np.append(input_pattern, self.input_during_run)
        
        return input_matrix

    def applyActivationFunction(self, matrix):
        return logistic.cdf(matrix)
    
    def takeInputFromSim(self, data):
        self.input_during_run = data
