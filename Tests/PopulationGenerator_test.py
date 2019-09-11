'''
Created on Sep 5, 2019

@author: alica
'''
import pytest
from MA.PopulationGenerator import PopulationGenerator
from MA.WalkingNetwork import WalkingNetwork


def test_mutate5050():
    pop_gen = PopulationGenerator(10, 53, 45)
    weights = WalkingNetwork.generateRandomWeights()
    nw = WalkingNetwork(weights)
    ten_networks = []
    for _i in range(0, 10):
        ten_networks.append(pop_gen.mutate5050(nw))
    assert nw in ten_networks, 'Always mutation (fails with 0.1%)'
    
    atleastOneChanged = False
    for i in range(0, 10):
        if(nw is not ten_networks[i]):
            atleastOneChanged = True
    assert atleastOneChanged, 'Never mutated (fails with 0.1%)'

    
def test_createNextGeneration():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    new_population = pop_gen.createNextGeneration(init_population)
    assert init_population[0] is new_population[0], 'Good networks not kept alive'
    assert init_population[1] is new_population[1], 'Good networks not kept alive'
    for i in range(2, 10):
        assert init_population[i] is not new_population[i], 'Unchanged WalkingNetwork'
    
    changedWeights = False
    for i in range(0, new_population[3].getNumberOfWeights()):
        if(init_population[0].getWeightAt(i) != new_population[3].getWeightAt(i)):
            changedWeights = True
    assert changedWeights, 'No changed Networkweights on nw in position 3'
        
    assert len(new_population) == 10, 'new population not the same size as old population'

    
def test_createMutantNetwork():
    pop_gen = PopulationGenerator(10, 53, 45)
    weights = WalkingNetwork.generateRandomWeights()
    nw = WalkingNetwork(weights)
    ten_networks = []
    for _i in range(0, 10):
        ten_networks.append(pop_gen.createMutantNetwork(nw))
    assert True == False, 'Test not implemented'


def test_crossoverNetwork():
    pop_gen = PopulationGenerator(10, 43, 45)
    weights = WalkingNetwork.generateRandomWeights()
    nw1 = WalkingNetwork(weights)
    weights = WalkingNetwork.generateRandomWeights()
    nw2 = WalkingNetwork(weights)
    crossover_network = pop_gen.crossoverNetwork(nw1, nw2)
    
    crossedOver = False
    for i in range(0, crossover_network.getNumberOfWeights()):
        if(crossover_network.getWeightAt(i) == nw1.getWeightAt(i)):
            assert not crossedOver, 'Switched back to nw1 (or weirder) (or really bad luck)'
        else:
            crossedOver = True
        
        if(crossedOver):
            assert crossover_network.getWeightAt(i) == nw2.getWeightAt(i), 'Weights from neither nw1 nor nw2 taken'
    
    
def test_getRandomIndexBetterPreferred():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    ten_choosen_indexes = []
    for _i in range(0, 10):
        ten_choosen_indexes.append(pop_gen.getRandomIndexBetterPreferred(init_population))
    individual_indexes = []
    for element in ten_choosen_indexes:
        if element not in individual_indexes:
            individual_indexes.append(element)
    assert len(ten_choosen_indexes) >= len(individual_indexes), 'no index chosen double, can happen but unlikely'  # TODO how unlikely
    assert init_population[0] in ten_choosen_indexes, 'first index not chosen, can happen but unlikely'  # TODO how unlikely

    
def test_initPopulation():
    pop_gen = PopulationGenerator(10, 53, 45)
    init_population = pop_gen.initPopulation()
    assert init_population[0] is not None, 'Generated WalkingNetwork is None'
    assert len(init_population) == 10, 'wrong amount of individuals in the init-population'

