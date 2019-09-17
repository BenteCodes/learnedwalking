'''
Created on 14.09.2019

@author: TKler
'''
from NIPSChallenge.GeneticAlgorithm import GeneticAlgorithm
import SafeData


def fullRun():
    cord = GeneticAlgorithm(5, 0, 0, 20)
    cord.population = loadpop()[:5]
    cord.evolve()


def loadpop():
    return SafeData.loadPopulation()


fullRun()
# pop = loadpop()
# print(pop[6].weights[119])
