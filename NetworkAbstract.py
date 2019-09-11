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

