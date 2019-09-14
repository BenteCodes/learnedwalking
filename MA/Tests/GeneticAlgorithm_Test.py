import pytest
from MA.GeneticAlgorithm import GeneticAlgorithm


def test_initNetwork():
    cord = GeneticAlgorithm(20, 50, 50, 20, 0)
    pass


# THIS IS NOT A UNIT TEST!!! ONLY MANUAL EXECUTION
def fullRun():
    cord = GeneticAlgorithm(6, 50, 50, 3, 0)
    cord.evolve()


fullRun()
