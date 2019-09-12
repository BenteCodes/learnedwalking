'''
Created on 12 Sep 2019

@author: felix
'''
from MA.PopulationGenerator import PopulationGenerator
from MA.FitnessFunction import FitnessFunction
from Tests.RobotControlDummy import RobotControlDummy
import SafeData
import numpy as np
from NewGAGeneral import NewGAGeneral


class GeneticAlgorithm(NewGAGeneral):

    number_of_steps_in_simulator = 400
    simulator_repetitions = 3

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, motor_number_flag):
        super()
        self.initRobotControl(motor_number_flag)
        
    def init_population(self):
        self.population = self.pop_generator.initPopulation()

    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)

    def initRobotControl(self, motor_number_flag):
        self.robot_control = RobotControlDummy(motor_number_flag)

    def initFitnessFunc(self):
        self.fitness_function = FitnessFunction()
        
    def calcFitness(self):
        

    @abstractmethod
    def getOutputFromSim(self):
        pass


