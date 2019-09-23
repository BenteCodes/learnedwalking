'''
Created on 19.09.2019

@author: TKler
'''
from NIPSChallenge.NIPSNetwork import NIPSNetwork
import numpy as np
from Network3LayerAbstract import Network3LayerAbstract


class SyncedNetwork(Network3LayerAbstract):
    
    def __init__(self, weights):
        self.weights = weights
        self.nw1 = NIPSNetwork(weights)
        self.nw2 = NIPSNetwork(weights)
        
        self.nw2.simple_pattern.increasePhaseByPI()
    
    def computeOneStep(self):
        output_part1 = self.nw1.computeOneStep()
        output_part2 = self.nw2.computeOneStep()
        
        return np.append(output_part1, output_part2)
    
    def resetHiddenLayer(self):
        self.nw1.resetHiddenLayer()
        self.nw2.resetHiddenLayer()
    
    def getWeightAt(self, index):
        return self.nw1.getWeightAt(index)
    
    def takeInputFromSim(self, data):
        pass
    
    @staticmethod
    def getNumberOfWeights():
        return NIPSNetwork.getNumberOfWeights()
    
    @staticmethod
    def generateRandomWeights():
        return NIPSNetwork.generateRandomWeights()
