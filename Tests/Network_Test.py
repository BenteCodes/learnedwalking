'''
Created on Sep 2, 2019

@author: alica
'''
import pytest
from Network import Network


def test_generateRandomWeights():
    weights = Network.generateRandomWeights()
    assert len(weights) == Network.number_of_weights, "Incorrect Number of weights"


def test_generateRandomNW():
    weights = Network.generateRandomWeights()
    nw = Network(weights)
    assert nw is not None


def test_initNetwork():
    weights = Network.generateRandomWeights()
    nw = Network(weights)
    assert nw is not None
    assert nw.number_of_input_units == 10, 'wrong number of input units'
    assert nw.number_of_hidden_units == 4, 'wrong number of hidden units'
    assert nw.number_of_output_units == 20, 'wrong number of output units'
    assert nw.are_there_non_zero_outputs_value == False, 'wrongly initialized are_there_non_zero_outputs_value'


def test_areThereNonZeroOutputs():
    weights = Network.generateRandomWeights()
    nw = Network(weights)
    assert nw.are_there_non_zero_outputs_value == False, 'are_there_non_zero_outputs_value wrongly set at the start'
    nw.areThereNonZeroOutput([0, 0, 0, 0])
    assert nw.are_there_non_zero_outputs_value == False, 'ZeroMovement not recognized'
    nw.areThereNonZeroOutput([-1, 1, 5, 9])
    assert nw.are_there_non_zero_outputs_value == True, 'Non-zero-movement not found'


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
