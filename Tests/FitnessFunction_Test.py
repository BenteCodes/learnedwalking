import pytest
from MA.FitnessFunction import FitnessFunction
from math import sqrt


def test_penalizeFalling():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.penalizeFalling(True) == -100, 'falling wrongly penalized'
    assert test_fitnessfunc.penalizeFalling(False) == 0, 'not falling penalized'


def test_calcDistanceMoved():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 1], [0, 1]) == 1, 'distance wrongly calculated'
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 2], [0, 1]) == 1.5, 'distance wrongly calculated'
    assert test_fitnessfunc.calcDistanceMoved([0, 0], [0, 1], [0, -1]) == 1, 'distance wrongly calculated'


def test_calcEuclideanDistance():
    test_fitnessfunc = FitnessFunction()
    assert test_fitnessfunc.calcEuclideanDistance([5, 3], [4, 1]) == sqrt(1 * 1 + 2 * 2)
    assert test_fitnessfunc.calcEuclideanDistance([38, -17], [8, 3]) == sqrt(30 * 30 + 20 * 20)
    assert test_fitnessfunc.calcEuclideanDistance([-15, -13], [-1, 8]) == sqrt(196 + 441)
