'''
Created on Sep 2, 2019

@author: alica
'''
import pytest
from MA.WalkingNetwork import WalkingNetwork
import numpy as np


def test_generateRandomWeights():
    weights = WalkingNetwork.generateRandomWeights()
    assert len(weights) == WalkingNetwork.number_of_weights, "Incorrect Number of weights"


def test_generateRandomNW():
    weights = WalkingNetwork.generateRandomWeights()
    nw = WalkingNetwork(weights)
    assert nw is not None


def test_initNetwork():
    weights = WalkingNetwork.generateRandomWeights()
    nw = WalkingNetwork(weights)
    assert nw is not None
    assert nw.number_of_input_units == 10, 'wrong number of input units'
    assert nw.number_of_hidden_units == 4, 'wrong number of hidden units'
    assert nw.number_of_output_units == 20, 'wrong number of output units'

    
def test_inputToHidden(): 
    hidden_to_hidden = [[1, 2, 3, 4]]
    last_output_hidden = [[1, 2, 3, 4]]
    nw_input = np.array([[1, 2, 3, 4]])
    weights = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    value_hidden_neurons = np.matmul(nw_input, weights)
        
    results = [10, 20, 30, 40]
    for index in range(0, 4):
        assert value_hidden_neurons[0][index] == results[index], 'wrong results'
        
    print('happy')
        
    for index in range(0, 4):  # append the hidden layer inputs. this has to be done one by one, as they are not fully connected, but just one weight per line
        value_hidden_neurons[0][index] += hidden_to_hidden[0][index] * last_output_hidden[0][index]
        
    results = [11, 24, 39, 56]
    for index in range(0, 4):
        assert value_hidden_neurons[0][index] == results[index], 'wrong results'
         
    print('happy')


def test_hiddenToOutput():
    last_output_hidden = [[5, 6, 7, 8]]
    hidden_to_output_all = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], ]
    value_output_neurons = np.matmul(last_output_hidden, hidden_to_output_all) 
    
    results = 26
    for index in range(0, 20):
        assert value_output_neurons[0][index] == (results * (index + 1)), 'wrong results'

    
def test_getInput():
    pass


def test_computeOneStep():
    pass


def test_resetHiddenLayer():
    pass


def test_getNumberOfWeights():
    pass


def test_getWeightAt():
    pass


def test_getMovement():
    pass
