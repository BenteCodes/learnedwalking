'''
Created on 11.09.2019

@author: TKler
'''
from builtins import staticmethod
'''
Created on 11.09.2019

@author: TKler
'''
from abc import abstractmethod, ABC
import numpy as np


class Network3LayerAbstract(ABC):

    @abstractmethod
    def computeOneStep(self):
        return NotImplementedError

    @abstractmethod
    def resetHiddenLayer(self):
        return NotImplementedError
    
    @abstractmethod
    def getWeightAt(self, index):
        return NotImplementedError
    
    @abstractmethod
    def takeInputFromSim(self, data):
        return NotImplementedError

    def initNetwork(self, weights):
        self.weights = weights
        self.last_output_hidden = []
        self.resetHiddenLayer() 
        
        position_start = 0
        position_end = self.number_of_input_units * self.number_of_hidden_units
        self.input_to_hidden_all = np.array([weights[position_start:position_end]])
        self.input_to_hidden_all = np.reshape(self.input_to_hidden_all, (self.number_of_input_units, self.number_of_hidden_units))

        position_start = position_end
        position_end += self.number_of_hidden_units        
        self.hidden_to_hidden = np.array([weights[position_start:position_end]])

        position_start = position_end
        position_end += (self.number_of_hidden_units * self.number_of_output_units)         
        self.hidden_to_output_all = np.array([weights[position_start:position_end]])
        self.hidden_to_output_all = np.reshape(self.hidden_to_output_all, (self.number_of_hidden_units, self.number_of_output_units))  # sort after connection not just a long list

    @staticmethod
    def getNumberOfWeights():
        return NotImplementedError
    
    @staticmethod
    def generateRandomWeights():
        return NotImplementedError
