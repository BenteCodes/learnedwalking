'''
Created on 12 Sep 2019

@author: felix
'''
from MA.PopulationGenerator import PopulationGenerator
from MA.FitnessFunction import FitnessFunction
from Tests.RobotControlDummy import RobotControlDummy
from NewGAGeneral import NewGAGeneral


class GeneticAlgorithmNew(NewGAGeneral):

    number_of_steps_in_simulator = 400
    simulator_repetitions = 3

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, motor_number_flag):
        super().__init__(popsize, mutation_rate, crossover_rate, iterations)
        self.robot_control.setMotorFlag(motor_number_flag)
        
    def init_population(self):
        self.population = self.pop_generator.initPopulation()

    def initPopGen(self, popsize, mutation_rate, crossover_rate):
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)

    def initRobotControl(self):
        self.robot_control = RobotControlDummy()

    def initFitnessFunc(self):
        self.fitness_function = FitnessFunction()
        
    def calcFitness(self, data):
        fitness = self.fitness_function.getFitness(data[0], data[1], data [2], data[3])
        return fitness

    def getOutputFromSim(self):
        passrobot_fell, start_point, pos_robot_foot_r, pos_robot_foot_l = self.robot_control.getEvalData()
        return passrobot_fell, start_point, pos_robot_foot_r, pos_robot_foot_l

