from scipy.stats import logistic
from NetworkTemplate import NetworkTemplate


class WalkingNetwork(NetworkTemplate):
    
    number_of_sensory_inputs = 0
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 4
    number_of_output_units = 20
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    start_weights_range = [-1, 1]

    # @input weights weights of the network
    def getInput(self):
        input_matrix = self.getInputFromSimplePattern()
        return input_matrix

    def applyActivationFunction(self, matrix):
        return (logistic.cdf(matrix) * 2) - 1

    def takeInputFromSim(self, data):
        pass  # not applicable as this does not take any input
