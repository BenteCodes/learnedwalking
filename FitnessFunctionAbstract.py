'''
Created on 11.09.2019

@author: TKler
'''
from abc import abstractmethod, ABC


class FitnessFunctionAbstract(ABC):
    
    @abstractmethod
    def getFitness(self):
        pass
