'''
Created on 11.09.2019

@author: TKler
'''
from abc import abstractmethod, ABC


class PopulationGeneratorAbstract(ABC):

    @abstractmethod
    def createNextGeneration(self, old_networks_sorted_by_fitness):
        return NotImplementedError
            
    @abstractmethod
    def initPopulation(self):
        return NotImplementedError
