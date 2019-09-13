'''
Created on 12 Sep 2019

@author: felix
'''

from abc import abstractmethod, ABC
import SafeData
import numpy as np


class NewGAGeneral(ABC):

    number_of_steps_in_simulator = 400
    simulator_repetitions = 3

    @abstractmethod
    def init_population(self):
        pass

    @abstractmethod        
    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        pass        

    @abstractmethod
    def initRobotControl(self):
        pass

    @abstractmethod
    def initFitnessFunc(self):
        pass

    @abstractmethod
    def calcFitness(self):
        pass

    @abstractmethod
    def getOutputFromSim(self):
        pass
    
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
        
        self.max_iterations = iterations
        
        self.initRobotControl()

        self.initPopGen(popsize, mutation_rate, crossover_rate)        
        self.init_population()
        
        self.initFitnessFunc()

    def simulateFitnessOfNetwork(self, network):
        # print('start simulation')
        self.robot_control.startSimulation()
        # print('start moving')
        self.walkInSimulator(network)
        
        dataDump = self.getOutputFromSim()
        
        fitness = self.calcFitness(dataDump)

        self.robot_control.stopSimulation()

        return fitness

    def walkInSimulator(self, network):
        for _i in range(0, self.number_of_steps_in_simulator):
            # data = self.robot_control.getOutput()
            # network.getInput(data)
            self.robot_control.walkRobot(network.computeOneStep())
            if(self.robot_control.robotFell()):
                break

    def getFitnessAveragedOverXTimes(self, network, times):
        fitness = 0
        for _1 in range(0, times):
            fitness += self.simulateFitnessOfNetwork(network)
            network.resetHiddenLayer()
        return fitness / times

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
        self.safeMeanAndTop5Fitnesses(meanFitness, fitnessList)
        
        # return only the ordered networks (best first)
        
        print([row[1] for row in fitnessList][:5])
        return [row[0] for row in fitnessList]

    def safeMeanAndTop5Fitnesses(self, mean_fitness, fitnessList):
        SafeData.safeMeanAndTop5Fitnesses(mean_fitness, [row[1] for row in fitnessList][:5])

    def safeNetwork(self, best_network):
        SafeData.safeNetwork(best_network)

    def evolve(self):
        for curr_it in range(0, self.max_iterations):
            rankedNetworks = self.getRankedNetworks()
            self.safeNetwork(rankedNetworks[0])
            self.population = self.pop_generator.createNextGeneration(rankedNetworks)
            print("Current iteration:" + str(curr_it + 1))
