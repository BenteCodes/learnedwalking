'''
Created on 12 Sep 2019

@author: felix
'''

from abc import abstractmethod, ABC
import SafeData
import numpy as np


class GeneticAlgorithmTemplate(ABC):

    number_of_steps_in_simulator = 100
    simulator_repetitions = 1
    number_of_documented_fitnesses_per_iteration = 5
    fall_foreward_action = np.array([1, 1, 0, 0, 0.5, 0, 0, 0, 0, 0, 0.5,
                                     0, 0, 1, 0, 0, 0.5, 0, 0, 0, 0, 0.5])

    @abstractmethod
    def init_population(self):
        return NotImplementedError

    @abstractmethod        
    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        return NotImplementedError        

    @abstractmethod
    def initRobotControl(self):
        return NotImplementedError

    @abstractmethod
    def initFitnessFunc(self):
        return NotImplementedError

    @abstractmethod
    def calcFitness(self):
        return NotImplementedError

    @abstractmethod
    def getEvalFromSim(self):
        return NotImplementedError
    
    def checkParameters(self, popsize, mutation_rate, crossover_rate, iterations):
        if popsize < 5:
            print("Paramcheck: Population size needs to be at least 5")
        if not 0 <= mutation_rate <= 100:
            print("Paramcheck: Mutation rate needs to be between 0 and 100")
        if not 0 <= crossover_rate <= 100:
            print("Paramcheck: Crossover rate needs to be between 0 and 100") 
        if iterations < 1:
            print("Paramcheck: iterations needs to be positive")

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations):
        self.checkParameters(popsize, mutation_rate, crossover_rate, iterations)
        
    def simulateFitnessOfNetwork(self, network):
        self.robot_control.startSimulation()
        self.walkInSimulator(network)
        
        dataDump = self.getEvalFromSim()
        
        fitness = self.calcFitness(dataDump)

        return fitness

    def walkInSimulator(self, network):
        for i in range(0, self.number_of_steps_in_simulator):
            if i <= 15:
                self.robot_control.walkRobot(self.fall_foreward_action)
            else:
                self.robot_control.walkRobot(network.computeOneStep())
            # sensor_data = self.robot_control.walkRobot(network.computeOneStep())
            # network.takeInputFromSim(sensor_data)
            if(self.robot_control.robotFell()):
                break

    def getFitnessAveragedOverXTimes(self, network, times):
        fitness = 0
        for _1 in range(0, times):
            fitness += self.simulateFitnessOfNetwork(network)
            network.resetHiddenLayer()
        return (fitness / times)

    def getRankedNetworks(self):  # get top5NWWithFitness
        fitnessList = []

        # create a list of networks their fitness
        for index in range(0, len(self.population)): 
            fitness = self.getFitnessAveragedOverXTimes(self.population[index], self.simulator_repetitions)
            fitnessList.append([self.population[index], fitness])
        
        # sort it after fitness, biggest firsts
        fitnessList.sort(key=lambda x: x[1], reverse=True)
        
        # compute mean fitness
        meanFitness = np.mean([row[1] for row in fitnessList], axis=0)
        # safe mean and top 5 fitnesses (no networks)
        self.safeMeanAndTopXFitnesses(meanFitness, fitnessList)
        
        # return only the ordered networks (best first)
        
        print([row[1] for row in fitnessList][:5])
        return [row[0] for row in fitnessList]

    def safeMeanAndTopXFitnesses(self, mean_fitness, fitnessList):
        SafeData.safeMeanAndTopXFitnesses(mean_fitness, [row[1] for row in fitnessList][:self.number_of_documented_fitnesses_per_iteration])

    def evolve(self):
        curr_it = 1
        while curr_it < 51:
            print("Current iteration:" + str(curr_it))
            rankedNetworks = self.getRankedNetworks()
            SafeData.safePopulation(self.population)
            self.population = self.pop_generator.createNextGeneration(rankedNetworks)
            curr_it += 1
