# Imports und so
from scipy.stats import logistic
from NetworkTemplate import NetworkTemplate
import random
from builtins import staticmethod


# class for that network
# parameters: weights
class WalkingNetwork(NetworkTemplate):
    
    number_of_sensory_inputs = 0
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 4
    number_of_output_units = 20
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)

    # @input weights weights of the network
    def getInput(self):
        input_matrix = self.getInputFromSimplePattern()
        return input_matrix

    def applySigmoidFunction(self, matrix):
        return (logistic.cdf(matrix) * 2) - 1

    def takeInputFromSim(self, data):
        pass  # not applicable as this does not take any input

    @staticmethod
    def getNumberOfWeights():
        return WalkingNetwork.number_of_weights
        
    @staticmethod
    def generateRandomWeights():
        weights = []
        for _i in range(0, WalkingNetwork.number_of_weights):
            weights.append(random.uniform(-1, 1))
            
        return weights
