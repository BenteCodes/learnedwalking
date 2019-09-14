import pytest
from MA.GeneticAlgorithm import GeneticAlgorithm
from MA.GA_New import GeneticAlgorithmNew


def test_initNetwork():
    cord = GeneticAlgorithm(20, 50, 50, 20, 0)
    pass


# THIS IS NOT A UNIT TEST!!! ONLY MANUAL EXECUTION
def fullRun():
    cord = GeneticAlgorithm(6, 50, 50, 3, 0)
    cord.evolve()


def fullRun2():
    cord = GeneticAlgorithmNew(6, 50, 50, 3, 0)
    cord.evolve()


fullRun()
fullRun2()
