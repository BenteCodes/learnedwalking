'''
Created on 11.09.2019

@author: TKler
'''
from MA.PopulationGenerator import PopulationGenerator
from NIPSChallenge.RobotControl import RobotControlNips
from NIPSChallenge.FitnessFunction import FitnessFunction
from GeneticAlgorithmTemplate import GeneticAlgorithmTemplate


class GeneticAlgorithm(GeneticAlgorithmTemplate):

    number_of_steps_in_simulator = 400  # FIXME
    simulator_repetitions = 1

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations):
        super().__init__(popsize, mutation_rate, crossover_rate, iterations)
        
    def init_population(self):
        self.population = self.pop_generator.initPopulation()

    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)

    def initRobotControl(self):
        self.robot_control = RobotControlNips()

    def initFitnessFunc(self):
        self.fitness_function = FitnessFunction()
        
    def calcFitness(self, data):
        fitness = self.fitness_function.getFitness(data)
        return fitness

    def getEvalFromSim(self):
        fitness = self.robot_control.getEvalData()
        return fitness
