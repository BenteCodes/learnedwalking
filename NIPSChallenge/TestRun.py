'''
Created on 14.09.2019

@author: TKler
'''
from NIPSChallenge.GeneticAlgorithm import GeneticAlgorithm
import SafeData


def fullRun():
    mutate = 80
    crossover = 20
    
    visualization = False
    pop_size = 20
    cord = GeneticAlgorithm(pop_size, mutate, crossover, 200000, visualization)
    cord.population = loadpop()#[:5]
    cord.evolve()


def loadpop():
    return SafeData.loadPopulation()


fullRun()

