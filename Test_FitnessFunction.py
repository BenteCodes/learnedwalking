import pytest
from FitnessFunction import FitnessFunction
from math import sqrt

def test_penalizeFalling():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.penalizeFalling([0, 0, 0.2]) == -100, 'falling wrongly penalized'
    assert test_fitnessfunc.penalizeFalling([0, 0, 0.5]) == 0, 'not falling penalized'

def test_penalizeNonMovement():
    pass

def test_calcDistanceMoved():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 1], [0, 1]) == 1, 'distance wrongly calculated'
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 2], [0, 1]) == 1.5, 'distance wrongly calculated'
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 1], [0, -1]) == 1, 'distance wrongly calculated'

def text_calcEuclideanDistance():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.calcEuclideanDistance([0, 0], [1, 1]) == sqrt(2)
    assert test_fitnessfunc.calcEuclideanDistance([1, 0], [1, 1]) == 1
    assert test_fitnessfunc.calcEuclideanDistance([1, 0], [-1, 0]) == 2