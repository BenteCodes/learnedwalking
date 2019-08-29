from WalkingNetwork import WalkingNetwork
from Populationgenerator import PopulationGenerator
from FitnessFunction import FitnessFunction
import SafeData
import random
import numpy as np
import math
import time
import csv


class Coordinator:

    def init_GA(self, popsize, mutation_rate, crossover_rate, iterations):
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.size_of_population = popsize
        self.current_iteration = 0
        self.max_iterations = iterations
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)
        

    def init_population(self, popsize):
        for i in range(0, popsize):     
            self.population.append(WalkingNetwork.createRandomNetwork())

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, motor_number_flag):
        self.population = []
        
        self.init_GA(popsize, mutation_rate, crossover_rate, iterations)
        
        self.initSimulation(motor_number_flag)
        
        self.motor_number_flag = motor_number_flag

        self.init_population(popsize)
        
        self.fitness_function = FitnessFunction()

    def obtainFitness(self, network):
        fitness = 0

        print('start simulation')
        self.robot_control.startSimulation()
        #print('start moving')
        self.walkInSimulator()
        
        position_robot, position_ref, position_robot_foot_r, position_robot_foot_l = self.robot_control.getEvalData()

        fitness = self.fitness_function.getFitness(network, position_robot, position_ref, position_robot_foot_r, position_robot_foot_l)

        #how fast did the robot move
        #distance / time_needed
        #fitness += #+velocity bonus
        print('fitness:' + str(fitness))
        
        self.robot_control.stopSimulation()
        print('stopped simulation')

        return fitness

        #walks in Simulator in scene XY
        # todo implement better stopvalue
    def walkInSimulator(self, network):
        #while self.shouldwalk:
        while True:
            motor_values = network.computeOneStepOnNw()
            self.robot_control.walkRobot(motor_values)
        

    def getFitnessAveragedOverXTimes(self, network, times):
        fitness = 0
        for x in range(0, times):
            fitness += self.obtainFitness(network)
            network.resetNetwork()
        
        fitness /= 3
        return fitness

    def getRankedNetworks(self):
        bestNetworks = []
        fitnessList = []

        for network in self.population:
            fitness = self.getFitnessAveragedOverXTimes(network, 3)
            fitnessList.append(fitness)

        indices = np.flipud(np.argsort(np.array(fitnessList)))
        meanfitness = np.mean(fitnessList)

        for index in indices:
            bestNetworks.append(self.population[index])

        self.safeFitness(meanfitness, bestFitness)

        np.array(sortby(x.axis,1))
        return bestNetworks


    def safeFitness(self, meanfitness, best5Fitness):
        SafeData.safeFitness(meanfitness, best5Fitness)

    def safeNetwork(self, network):
        SafeData.safeNetwork(network)

    def evolve(self):
        while self.current_iteration < self.max_iterations:
            rankedNetworks = self.getRankedNetworks()
            self.pop_generator.createNextGeneration(rankedNetworks)
            self.current_iteration += 1
            self.safeNetwork(rankedNetworks[0])
            print(self.current_iteration)
