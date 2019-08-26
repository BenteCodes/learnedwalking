
import WalkingNetwork
import random
import numpy as np
import vrep
import math
import time
import csv
from nicomotion import Motion


# genetic algorithm to learn basic pattern
class GA_Gait:
    networksize = 124
    factor = 1
    robot_string = "../json/nico_humanoid_full_with_grippers_unchecked.json"
# initialize randomly 20 networks of type 1

    def initSimulation(self):
        self.robot = Motion.Motion(robot_string, vrep=True, vrepHost='127.0.0.1', vrepPort=19997)
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 19996, True, True, 5000, 5)


    def init_GA(self, popsize, mutation_rate, crossover_rate, iterations):
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.size_of_population = popsize
        self.current_iteration = 0
        self.max_iterations = iterations


    def init_population(self, popsize):
        i = 0
        j = 0 #todo Adapt to walking_network
        while i < popsize:
            weights = []
            while j < self.networksize:
                weights.append(random.uniform(-1, 1))
                j += 1
            
            new_network = WalkingNetwork.WalkingNetwork(weights, self.robot, self.clientID, self.motor_factor)
            self.population.append(new_network)
            self.ranking.append(popsize - i)
            i += 1
            j = 0

    def __init__(self, popsize, mutation_rate, crossover_rate, iterations, motor_factor):
        self.population = []
        self.ranking = []
        
        self.init_GA(popsize, mutation_rate, crossover_rate, iterations)
        
        self.initSimulation()
        
        self.motor_factor = motor_factor

        self.init_population(popsize)

# define fitness function (maybe from parameter)

# map fittness function and output to get the error

    def penalizeFalling(self, position_robot):
        if position_robot[2] < 0.4: # robotFellDownThreshold
            fitness -= 100 #relly don't fall
        return fitness


    def penalizeNonMovement(self, network):
        if network.highest_angle == 0: #if there is 0 movement
            fitness -= 2000
        return fitness


    def calcDistanceMoved(self, position_ref, position_robot_foot_r, position_robot_foot_l):
        distance_r = math.sqrt((math.pow((position_ref[0] - position_robot_foot_r[0]), 2)) + (math.pow((position_ref[1] - position_robot_foot_r[1]), 2)) + (math.pow((position_ref[2] - position_robot_foot_r[2]), 2)))
        distance_l = math.sqrt((math.pow((position_ref[0] - position_robot_foot_l[0]), 2)) + (math.pow((position_ref[1] - position_robot_foot_l[1]), 2)) + (math.pow((position_ref[2] - position_robot_foot_l[2]), 2)))
        fitness += (distance_l + distance_r) / 2
        return fitness


    def stopSimulation(self, vrep):
        return vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)


    def startSimulation(self):
        time.sleep(0.5)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.5)


    def getEvalData(self):
        cube_handle = vrep.simxGetObjectHandle(self.clientID, "reference_cube", vrep.simx_opmode_oneshot_wait)
        [m, position_ref] = vrep.simxGetObjectPosition(self.clientID, cube_handle[1], -1, vrep.simx_opmode_oneshot_wait) #print(position_ref)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "right_foot_11_respondable", vrep.simx_opmode_oneshot_wait)
        [m, position_robot_foot_r] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, vrep.simx_opmode_oneshot_wait)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "left_foot_11_respondable", vrep.simx_opmode_oneshot_wait)
        [m, position_robot_foot_l] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, vrep.simx_opmode_oneshot_wait) #print(position_robot_foot)
        torso_handle = vrep.simxGetObjectHandle(self.clientID, "torso_11_visual", vrep.simx_opmode_oneshot_wait)
        [m, position_robot] = vrep.simxGetObjectPosition(self.clientID, torso_handle[1], -1, vrep.simx_opmode_oneshot_wait)
        return position_robot, position_ref, position_robot_foot_r, position_robot_foot_l

    def obtainFitness(self, network):
        fitness = 0

        print('start simulation')
        self.startSimulation()
        #print('start moving')
        network.walkRobot()
        position_robot, position_ref, position_robot_foot_r, position_robot_foot_l = self.getEvalData()

        fitness = self.penalizeNonMovement(network)

        fitness = self.penalizeFalling(position_robot)

        fitness = self.calcDistanceMoved(position_ref, position_robot_foot_r, position_robot_foot_l)
        #how fast did the robot move
        #distance / time_needed
        #fitness += #+velocity bonus
        print('fitness:' + str(fitness))
        
        self.stopSimulation(vrep)
        print('stopped simulation')

        return fitness



    def runXTimes(self, network, times):
        fitness = 0
        for x in range(0, times):
            fitness += self.obtainFitness(network)
            network.resetNetwork()
        
        fitness /= 3
        return fitness

    def getBestNetworks(self):

        bestNetworks = []
        fitnessList = []

        for network in self.population:
            fitness = self.runXTimes(network, 3)
            fitnessList.append(fitness)

        indices = np.flipud(np.argsort(np.array(fitnessList)))
        meanfitness = np.mean(fitnessList)

        for index in indices:
            bestNetworks.append(self.population[index])

        self.safeFitness(meanfitness, bestFitness)

        np.array(sortby(x.axis,1))
        return bestNetworks

    def getRandomIndexBetterPreferred(self):
        #print('selection')
        maximum = sum(range(self.size_of_population + 1))
        pick = random.uniform(0, maximum)
        
        current = 0
        counter = self.size_of_population
        for i in range(0, len(self.ranking)):
            current += counter
            if current >= pick:
                return i
            counter -= 1


    # create the next generation
    def createNextGeneration(self, bestNetworks):
        print('Next Generation')
        self.population = []
        bestNetworks[0].resetNetwork()
        bestNetworks[1].resetNetwork()
        self.population.append(bestNetworks[0])
        self.population.append(bestNetworks[1])

        while len(self.population) < self.size_of_population:
            probability = random.randint(0, 100)
            #crossover with probable mutation
            if probability <= self.crossover_rate:
                child_network = self.crossoverNetwork(bestNetworks[self.getRandomIndexBetterPreferred()], bestNetworks[self.getRandomIndexBetterPreferred()])
                mutate = random.randint(0, 1)
                if mutate == 1:
                    self.createMutantNetwork(child_network)
                    self.population.append(child_network)
                    continue
            else:
                #only mutation
                #print(m)
                #print(len(best5Networks))
                child_network = self.createMutantNetwork(bestNetworks[self.getRandomIndexBetterPreferred()])
                self.population.append(child_network)
        #print(self.population)

    def createMutantNetwork(self, network):
        new_weights = []
        for weight in network.weights:
            # probability to mutate into weightmutation
            if random.randint(1, 100) <= self.mutation_rate:
                mutation = random.uniform(-self.factor, self.factor)
                weight = weight + mutation
            new_weights.append(weight)
        child_network = WalkingNetwork.WalkingNetwork(new_weights, self.robot, self.clientID, self.motor_factor)
        return child_network

    def crossoverNetwork(self, network1, network2):
        crossover_point = random.randint(0, self.networksize)
        new_weights = []
        fill = 0
        while fill < self.networksize:
            if fill <= crossover_point:
                #print(fill)
                new_weights.append(network1.weights[fill])
                fill = fill + 1
            else:
                new_weights.append(network2.weights[fill])
                fill = fill + 1
        child_network = WalkingNetwork.WalkingNetwork(new_weights, self.robot, self.clientID, self.motor_factor)
        return child_network

    def safeFitness(self, meanfitness, best5Fitness):
        with open('fitnessmoremotors_static.csv', 'a') as csvfile1:
            errorwriter = csv.writer(csvfile1, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            errorwriter.writerow([str(self.current_iteration), str(meanfitness), str(best5Fitness[0]), str(best5Fitness[1]), str(best5Fitness[2]), str(best5Fitness[3]), str(best5Fitness[4])])


    def safeNetwork(self, network):
        with open('networkmoremotors_static.csv', 'wb') as csvfile:
            weightwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            weightstring = []
            for weight in network.weights:
                weightstring.append(str(weight) + ',')
            weightwriter.writerow(weightstring)

    def evolve(self):
        while self.current_iteration < self.max_iterations:
            bestNetworks = self.getBestNetworks()
            self.createNextGeneration(bestNetworks)
            self.current_iteration = self.current_iteration + 1
            self.safeNetwork(bestNetworks[0])
            print(self.current_iteration)



testGA = GA_Gait(150, 20, 10, 10000, 0)
GA_Gait.evolve(testGA)
