'''
Created on Sep 5, 2019

@author: alica
'''
import pytest
from PopulationGenerator import PopulationGenerator
from Network import Network


def test_mutate5050():
    pop_gen = PopulationGenerator(10, 53, 45)
    weights = Network.generateRandomWeights()
    nw = Network(weights)
    ten_networks = []
    for i in range(0, 10):
        ten_networks.append(pop_gen.mutate5050(nw))
    assert nw in ten_networks, 'Always mutation'
    
    assert True == False, 'Test not implemented'

    
def test_createNextGeneration():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    new_population = pop_gen.createNextGeneration(init_population)
    assert init_population[0] is new_population[0], 'Good networks not kept alive'
    assert len(new_population) == 10, 'new population not the same size as old population'

    
def test_createMutantNetwork():
    pop_gen = PopulationGenerator(10, 53, 45)
    weights = Network.generateRandomWeights()
    nw = Network(weights)
    ten_networks = []
    for i in range(0, 10):
        ten_networks.append(pop_gen.createMutantNetwork(nw))
    assert True == False, 'Test not implemented'


def test_crossoverNetwork():
    pop_gen = PopulationGenerator(10, 43, 45)
    weights = Network.generateRandomWeights()
    nw1 = Network(weights)
    weights = Network.generateRandomWeights()
    nw2 = Network(weights)
    crossover_network = pop_gen.crossoverNetwork(nw1, nw2)
    for i in range(0, crossover_network.getNumberOfWeights()):
        assert crossover_network.getWeightAt(i) in [nw1.getWeightAt(i), nw2.getWeightAt(i)], 'Crossover did not work'

    
def test_getRandomIndexBetterPreferred():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    ten_choosen_indexes = []
    for i in range(0, 10):
        ten_choosen_indexes.append(pop_gen.getRandomIndexBetterPreferred(init_population))
    individual_indexes = []
    for element in ten_choosen_indexes:
        if element not in individual_indexes:
            individual_indexes.append(element)
    assert len(ten_choosen_indexes) >= len(individual_indexes), 'no index chosen double, can happen but unlikely'
    assert init_population[0] in ten_choosen_indexes, 'first index not chosen, can happen but unlikely'

    
def test_initPopulation():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    assert init_population[0] is not None, 'Generated Network is None'
    assert len(init_population) == 10, 'wrong amount of individuals in the init-population'

