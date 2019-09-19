'''
Created on 19.09.2019

@author: TKler
'''
from NIPSChallenge.NIPSNetwork import NIPSNetwork
import numpy as np


class Syncednetwork(NIPSNetwork):
    
    number_of_sensory_inputs = 0
    number_of_pattern_inputs = 4
    number_of_input_units = number_of_pattern_inputs + number_of_sensory_inputs
    number_of_hidden_units = 11
    number_of_output_units = 11
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    start_weights_range = [-8, 8]

    def __init__(self, weights):
        self.nw1 = NIPSNetwork(weights)
        self.nw2 = NIPSNetwork(weights)
        
        self.nw2.simple_pattern = self.nw1.simple_pattern.increasePhaseByPI()
    
    def computeOneStep(self):
        output_part1 = self.nw1.computeOneStep()
        output_part2 = self.nw2.computeOneStep()
        
        return np.concatenate(output_part1, output_part2, axis=0)
    
    def resetHiddenLayer(self):
        self.nw1.resetHiddenLayer()
        self.nw2.resetHiddenLayer()
    
    def getWeightAt(self, index):
        return self.nw1.getWeightAt(index)
    
