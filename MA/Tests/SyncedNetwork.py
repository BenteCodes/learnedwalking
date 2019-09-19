'''
Created on 19.09.2019

@author: TKler
'''
from NIPSChallenge.SyncedNetwork import SyncedNetwork
from NIPSChallenge.NIPSNetwork import NIPSNetwork


def sync_test():
    weights = SyncedNetwork.generateRandomWeights()
    synced = SyncedNetwork(weights)
    
    # assert synced.nw2.simple_pattern.currentstep == (synced.nw1.simple_pattern..currentstep + 50)
    
    # synced.nw2.simple_pattern = synced.nw2.simple_pattern.returnWithIncreasePhaseByPI()
    
    # assert synced.nw2.simple_pattern.currentstep == synced.nw1.simple_pattern.currentstep
    
    array = synced.computeOneStep()
    half = int(len(array) / 2)
    
    array2 = array[half :]
    array = array [0 : half]
    print(array)
    print(array2)
    for i in range(0, len(array) - 1):
        assert abs(array[i] - array2[i]) < 0.1, 'non equal values'


sync_test()


def testing():
    weights = NIPSNetwork.generateRandomWeights()
    nw1 = NIPSNetwork(weights)
    nw2 = NIPSNetwork(weights)
    
    array1 = nw1.computeOneStep()
    array2 = nw2.computeOneStep()
    
    print(array1)
    print(array2)
    for i in range(0, len(array1) - 1):
        assert (array1[i] == array2[i]), 'non equal values'  

