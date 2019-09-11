'''
Created on 11.09.2019

@author: TKler
'''
from MA.PopulationGenerator import PopulationGenerator
from RobotControlAbstract import RobotControlAbstract
from FitnessFunctionAbstract import FitnessFunctionAbstract
import numpy as np
import SafeData
from GeneticAlgorithmAbstract import GeneticAlgorithmAbstract


class GeneticAlgorithm(GeneticAlgorithmAbstract):

    number_of_steps_in_simulator = 1  # TODO
    simulator_repetitions = 1

    def init_population(self):
        self.population = self.pop_generator.initPopulation()
            
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
        
        self.robot_control = RobotControlAbstract()  # TODO
        # self.robot_control = DummyRobotControl()
        
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)
        self.init_population()
        
        self.fitness_function = FitnessFunctionAbstract()  # TODO

    def simulateFitnessOfNetwork(self, network):
        # print('start simulation')
        self.robot_control.startSimulation()
        # print('start moving')
        self.walkInSimulator(network)
        
        TODOVARIABLE = self.robot_control.getEvalData()

        fitness = TODOVARIABLE[0]
        
        self.robot_control.stopSimulation()
        # print('stopped simulation')

        return fitness

    # todo implement better stopvalue
    def walkInSimulator(self, network):
        if network is None:
            print('None found')
        for _i in range(0, self.number_of_steps_in_simulator):
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
        
        # sort it after fitnes, biggest firsts
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
