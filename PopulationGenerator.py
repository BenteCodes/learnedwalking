import WalkingNetwork
import random

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

    def createNextGeneration(self, networks_sorted_by_fitness):
        print('Next Generation')
        population = []
        population.append(networks_sorted_by_fitness[0].resetHiddenLayer())
        population.append(networks_sorted_by_fitness[1].resetHiddenLayer())

        while len(population) < self.size_of_population:
            probability = random.randint(0, 100)
            #crossover with 5050 mutation
            if probability <= self.crossover_rate:
                child_network = self.crossoverNetwork(self.getRandomIndexBetterPreferred(networks_sorted_by_fitness), self.getRandomIndexBetterPreferred(networks_sorted_by_fitness))
                child_network = self.mutate5050(child_network)
            else:
                #only mutation
                child_network = self.createMutantNetwork(self.getRandomIndexBetterPreferred(networks_sorted_by_fitness))
            
            population.append(child_network)
                

    def createMutantNetwork(self, network):
        new_weights = []
        for index in range(0, network.getSize()):
            # probability to mutate into weightmutation
            weight = network.getWeightAt(index)
            if random.randint(0, 100) <= self.mutation_rate:
                mutation = random.uniform(-self.max_weight_change, self.max_weight_change)
                weight += mutation
            new_weights.append(weight)
            
        return WalkingNetwork(new_weights)

    def crossoverNetwork(self, network1, network2):
        network_size = network1.getNumberOfWeights()
        crossover_point = random.randint(0, network_size-1)
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
        