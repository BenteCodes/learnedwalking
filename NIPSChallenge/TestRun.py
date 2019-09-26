'''
Created on 14.09.2019

@author: TKler
'''
from NIPSChallenge.GeneticAlgorithm import GeneticAlgorithm
import SafeData


def fullRun():
    visualization = False
    cord = GeneticAlgorithm(20, 50, 50, 200000, visualization)
    #cord.population = loadpop()[:5]
    cord.evolve()


def loadpop():
    return SafeData.loadPopulation()


fullRun()

