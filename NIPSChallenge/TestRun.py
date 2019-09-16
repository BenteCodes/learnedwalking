'''
Created on 14.09.2019

@author: TKler
'''
from NIPSChallenge.GeneticAlgorithm import GeneticAlgorithm
import SafeData


def fullRun():
    cord = GeneticAlgorithm(10, 50, 50, 20)
    cord.population = loadpop()
    cord.evolve()


def loadpop():
    return SafeData.loadPopulation()


fullRun()
# pop = loadpop()
# print(pop[6].weights[119])
