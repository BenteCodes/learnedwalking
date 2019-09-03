from Network import Network
from PopulationGenerator import PopulationGenerator
from FitnessFunction import FitnessFunction
from Tests.RobotControlDummy import RobotControlDummy
import SafeData


class Coordinator:

    number_of_steps_in_simulator = 400

    def init_population(self, popsize):
        for _1 in range(0, popsize):     
            self.population.append(Network(Network.generateRandomWeights()))
            
    def checkParameters(self, popsize, mutation_rate, crossover_rate, iterations, motor_number_flag):
        if popsize < 3:
            print("Paramcheck: Population size needs to be at least 2")
        if 0 <= mutation_rate <= 100:
            print("Paramcheck: Mutation rate needs to be between 0 and 100")
        if 0 <= crossover_rate <= 100:
            print("Paramcheck: Crossover rate needs to be between 0 and 100") 
        if iterations < 1:
            print("Paramcheck: iterations need to be positive")
        if not((-1 < motor_number_flag) and (motor_number_flag < 3)):
            print("Paramcheck: Wrong motor number flag, only 0,1,2 allowed")

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, motor_number_flag):
        self.checkParameters(popsize, mutation_rate, crossover_rate, iterations, motor_number_flag)
        self.population = []
        self.max_iterations = iterations
        
        self.pop_generator = PopulationGenerator(popsize, mutation_rate, crossover_rate)
        
        self.robot_control = RobotControlDummy(motor_number_flag)
        # self.robot_control = DummyRobotControl()

        self.init_population(popsize)
        
        self.fitness_function = FitnessFunction()

    def obtainFitness(self, network):
        print('start simulation')
        self.robot_control.startSimulation()
        # print('start moving')
        self.walkInSimulator(network)
        
        robot_fell, start_point, pos_robot_foot_r, pos_robot_foot_l = self.robot_control.getEvalData()

        fitness = self.fitness_function.getFitness(network.areThereNonZeroOutputs(), robot_fell, start_point, pos_robot_foot_r, pos_robot_foot_l)

        # how fast did the robot move
        # distance / time_needed
        # fitness += #+velocity bonus
        print('fitness:' + str(fitness))
        
        self.robot_control.stopSimulation()
        print('stopped simulation')

        return fitness

    # todo implement better stopvalue
    def walkInSimulator(self, network):
        for _i in range(0, self.number_of_steps_in_simulator):
            self.robot_control.walkRobot(network.computeOneStepOnNw())
            if(self.robot_control.robotFell()):
                break

    def getFitnessAveragedOverXTimes(self, network, times):
        fitness = 0
        for _1 in range(0, times):
            fitness += self.obtainFitness(network)
            network.resetNetwork()
        return fitness / 3

    def getRankedNetworks(self):  # get top5NWWithFitness
        fitnessList = []

        for index in range(0, len(self.population)):
            fitness = self.getFitnessAveragedOverXTimes(self.population[index], 3)
            fitnessList.append([self.population[index], fitness])
        
        fitnessList.sort(key=lambda x: x[1], reverse=True)
        
        meanFitness = map(lambda x:sum(x) / float(len(x)), zip(*fitnessList))[1]

        self.safeMeanAndTop5Fitnesses(meanFitness, [row[1] for row in fitnessList][:5])

        return [row[0] for row in fitnessList]

    def safeMeanAndTop5Fitnesses(self, meanfitness, best5Fitnesses):
        SafeData.safeMeanAndTop5Fitnesses(meanfitness, best5Fitnesses)

    def safeNetwork(self, network):
        SafeData.safeNetwork(network)

    def evolve(self):
        for curr_it in range(0, self.max_iterations):
            rankedNetworks = self.getRankedNetworks()
            self.pop_generator.createNextGeneration(rankedNetworks)
            self.safeNetwork(rankedNetworks[0])
            print("Current iteration:" + curr_it)
