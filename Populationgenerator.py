import WalkingNetwork
import random
import numpy as np
import math




# genetic algorithm to learn basic pattern
class PopulationGenerator:

    max_weight_change = 1

    def __init__(self, size_of_population, mutation_rate, crossover_rate):
        self.size_of_population = size_of_population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
               
    # create the next generation

    def mutate5050(self, child_network):
        mutate = random.randint(0, 1)
        if mutate == 1:
            self.createMutantNetwork(child_network)
        return child_network

    def createNextGeneration(self, rankedNetworks):
        print('Next Generation')
        population = []
        population.append(rankedNetworks[0].resetHiddenLayer())
        population.append(rankedNetworks[1].resetHiddenLayer())

        while len(population) < self.size_of_population:
            probability = random.randint(0, 100)
            #crossover with 5050 mutation
            if probability <= self.crossover_rate:
                child_network = self.crossoverNetwork(getRandomIndexBetterPreferred(rankedNetworks), getRandomIndexBetterPreferred(rankedNetworks))
                child_network = self.mutate5050(child_network)
            else:
                #only mutation
                child_network = self.createMutantNetwork(getRandomIndexBetterPreferred(rankedNetworks))
            
            population.append(child_network)
                

    def createMutantNetwork(self, network):
        new_weights = []
        for weight in network.getWeights():
            # probability to mutate into weightmutation
            if random.randint(0, 100) <= self.mutation_rate:
                mutation = random.uniform(-self.max_weight_change, self.max_weight_change)
                weight += mutation
            new_weights.append(weight)
            
        return network.newNWWithDifferentWeights(new_weights)

    def crossoverNetwork(self, network1, network2):
        crossover_point = random.randint(0, network1.getNumberOfWeights())
        new_weights = []
        for index in range(0, self.networksize):
            if index <= crossover_point:
                new_weights.append(network1.weights[index])
            else:
                new_weights.append(network2.weights[index])
            index += 1
        return network1.newNWWithDifferentWeights(new_weights)
    
    def getRandomIndexBetterPreferred(self, ranked):
        rankSum = sum(range(self.size_of_population + 1))
        pickedIndex = random.uniform(0, rankSum)
        
        curIndex = 0
        diminishingWorth = self.size_of_population
        for i in range(0, size_of_population):
            curIndex += diminishingWorth
            if curIndex >= pickedIndex:
                return ranked[i]
            diminishingWorth -= 1
        