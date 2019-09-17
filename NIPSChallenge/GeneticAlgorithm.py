'''
Created on 11.09.2019

@author: TKler
'''
from NIPSChallenge.PopGenNips import PopulationGeneratorNips
from NIPSChallenge.RobotControl_local import RobotControlNipsLocal
from NIPSChallenge.FitnessFunction import FitnessFunction
from GeneticAlgorithmTemplate import GeneticAlgorithmTemplate


class GeneticAlgorithm(GeneticAlgorithmTemplate):

    number_of_steps_in_simulator = 200 
    simulator_repetitions = 1

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, visualization):
        super().checkParameters(popsize, mutation_rate, crossover_rate, iterations)
        
        self.max_iterations = iterations
        
        self.initRobotControl(visualization)

        self.initPopGen(popsize, mutation_rate, crossover_rate)        
        self.init_population()
        
        self.initFitnessFunc()
        
    def init_population(self):
        self.population = self.pop_generator.initPopulation()

    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        self.pop_generator = PopulationGeneratorNips(popsize, mutation_rate, crossover_rate)

    def initRobotControl(self, visualization):
        self.robot_control = RobotControlNipsLocal(visualization)

    def initFitnessFunc(self):
        self.fitness_function = FitnessFunction()
        
    def calcFitness(self, data):
        fitness = self.fitness_function.getFitness(data)
        return fitness

    def getEvalFromSim(self):
        fitness = self.robot_control.getEvalData()
        return fitness
