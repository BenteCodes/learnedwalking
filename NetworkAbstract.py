'''
Created on 11.09.2019

@author: TKler
'''
'''
Created on 11.09.2019

@author: TKler
'''
from abc import abstractmethod, ABC


class NetworkAbstract(ABC):

    @abstractmethod
    def computeOneStep(self):
        pass

    @staticmethod
    def generateRandomWeights():
        pass
    # I wowuld like to define this as a default method here, but I am incapable of getting a default variable here
