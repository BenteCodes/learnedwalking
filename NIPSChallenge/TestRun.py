'''
Created on 14.09.2019

@author: TKler
'''
from NIPSChallenge.GeneticAlgorithm import GeneticAlgorithm


def fullRun():
    cord = GeneticAlgorithm(6, 50, 50, 3)
    cord.evolve()


fullRun()
