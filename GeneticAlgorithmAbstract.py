'''
Created on 11.09.2019

@author: TKler
'''
from abc import abstractmethod, ABC


class GeneticAlgorithmAbstract(ABC):

    @abstractmethod
    def evolve(self):
        pass
