from MA.WalkingNetwork import WalkingNetwork
from PopulationGeneratorAbstract import PopulationGeneratorAbstract 
import random


# genetic algorithm to learn basic pattern
class PopulationGenerator(PopulationGeneratorAbstract):

    max_weight_change = 1
    number_of_kept_best_networks = 2

    def __init__(self, size_of_population, mutation_rate, crossover_rate):
        self.size_of_population = size_of_population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
               
    # create the next generation

    def mutate5050(self, network):
        mutate = random.randint(0, 1)
        if mutate == 1:
            network = self.createMutantNetwork(network)
        return network

    def createNextGeneration(self, old_networks_sorted_by_fitness):
        print('Next Generation')
        new_population = []
        
        for i in range(0, self.number_of_kept_best_networks):
            old_networks_sorted_by_fitness[i].resetHiddenLayer()
            new_population.append(old_networks_sorted_by_fitness[i])
        
        while len(new_population) < self.size_of_population:
            probability = random.randint(0, 100)
            # crossover with 5050 mutation
            if probability <= self.crossover_rate:
                child_network = self.crossoverNetwork(self.getRandomIndexBetterPreferred(old_networks_sorted_by_fitness), self.getRandomIndexBetterPreferred(old_networks_sorted_by_fitness))
                child_network = self.mutate5050(child_network)
            else:
                # only mutation
                child_network = self.createMutantNetwork(self.getRandomIndexBetterPreferred(old_networks_sorted_by_fitness))
            
            new_population.append(child_network)
        
        return new_population

    def createMutantNetwork(self, network):
        new_weights = []
        for index in range(0, network.getNumberOfWeights()):
            # probability to mutate into weightmutation
            weight = network.getWeightAt(index)
            if random.randint(0, 100) <= self.mutation_rate:
                mutation = random.uniform(-self.max_weight_change, self.max_weight_change)
                weight += mutation
            new_weights.append(weight)
            
        return WalkingNetwork(new_weights)

    def crossoverNetwork(self, network1, network2):
        network_size = network1.getNumberOfWeights()
        crossover_point = random.randint(0, network_size - 1)
        new_weights = []
        for index in range(0, network_size):
            if index <= crossover_point:
                new_weights.append(network1.getWeightAt(index))
            else:
                new_weights.append(network2.getWeightAt(index))
        return WalkingNetwork(new_weights)
    
    def getRandomIndexBetterPreferred(self, ranked):
        rankSum = sum(range(self.size_of_population + 1))
        pickedIndex = random.uniform(0, rankSum)
        
        curIndex = 0
        diminishingWorth = self.size_of_population
        for i in range(0, self.size_of_population):
            curIndex += diminishingWorth
            if curIndex >= pickedIndex:
                return ranked[i]
            diminishingWorth -= 1
            
    def initPopulation(self):
        population = []
        for _1 in range(0, self.size_of_population):     
            population.append(WalkingNetwork(WalkingNetwork.generateRandomWeights()))
        
        return population
        
