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

    @staticmethod
    def getNumberOfWeights():
        return NotImplementedError
    
    @staticmethod
    def generateRandomWeights():
        return NotImplementedError
