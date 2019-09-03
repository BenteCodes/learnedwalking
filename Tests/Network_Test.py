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
