'''
Created on 11.09.2019

@author: TKler
'''
from scipy.stats import logistic
from NetworkTemplate import NetworkTemplate


class NIPSNetwork(NetworkTemplate):
    
    number_of_sensory_inputs = 0
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 11
    number_of_output_units = 11
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    start_weights_range = [-8, 8]
    
    def getInput(self):
        return self.getInputFromSimplePattern()

    def applyActivationFunction(self, matrix):
        return logistic.cdf(matrix)
    
    def takeInputFromSim(self, data):
        pass
