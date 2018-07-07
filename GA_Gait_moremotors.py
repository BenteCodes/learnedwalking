
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
# initialize randomly 20 networks of type 1
    def __init__(self, size, mutation_rate, crossover_rate, iterations, step):
        self._population = []
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.size_of_population = size
        self.current_iteration = 0
        self.max_iterations = iterations
        self.robot = Motion.Motion("../json/nico_humanoid_full_with_grippers_unchecked.json", vrep=True, vrepHost='127.0.0.1', vrepPort=19997)
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 19996, True, True, 5000, 5)
        print(self.clientID)
        self.ranking = []
        self.networksize = 124
        self.factor = 1
        self.step = step

        i = 0
        j = 0
        #todo Adapt to walking_network
        while i < size:
            weights = []
            while j < self.networksize:
                weights.append(random.uniform(-10, 10))
                j = j + 1
            new_network = WalkingNetwork.WalkingNetwork(weights, self.robot, self.clientID, self.step)
            self._population.append(new_network)
            self.ranking.append(size-i)
            i = i + 1
            j = 0

# define fitness function (maybe from parameter)

# map fittness function and output to get the error
    def calculateFitness(self, network):
        fitness = 0

        print('start simulation')
        time.sleep(0.5)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.5)
        #print('start moving')
        network.walkRobot()
        cube_handle = vrep.simxGetObjectHandle(self.clientID, "reference_cube", vrep.simx_opmode_oneshot_wait)
        [m, position_ref] = vrep.simxGetObjectPosition(self.clientID, cube_handle[1], -1, vrep.simx_opmode_oneshot_wait)
        #print(position_ref)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "right_foot_11_respondable", vrep.simx_opmode_oneshot_wait)
        [m, position_robot_foot_r] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, vrep.simx_opmode_oneshot_wait)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "left_foot_11_respondable", vrep.simx_opmode_oneshot_wait)
        [m, position_robot_foot_l] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, vrep.simx_opmode_oneshot_wait)
        #print(position_robot_foot)
        torso_handle = vrep.simxGetObjectHandle(self.clientID, "torso_11_visual", vrep.simx_opmode_oneshot_wait)
        [m, position_robot] = vrep.simxGetObjectPosition(self.clientID, torso_handle[1], -1, vrep.simx_opmode_oneshot_wait)

        #print(network.highest_angle)
        #was at least one joint moved
        if network.highest_angle == 0:
            fitness = -2000

        if position_robot[2] < 0.4:
            fitness = fitness - 1.2

        #how far did the robot move
        distance_r = math.sqrt((math.pow((position_ref[0]-position_robot_foot_r[0]), 2)) + (math.pow((position_ref[1]-position_robot_foot_r[1]), 2)) + (math.pow((position_ref[2]-position_robot_foot_r[2]),2)))
        distance_l = math.sqrt((math.pow((position_ref[0]-position_robot_foot_l[0]), 2)) + (math.pow((position_ref[1]-position_robot_foot_l[1]), 2)) + (math.pow((position_ref[2]-position_robot_foot_l[2]),2)))
        fitness = fitness + ((distance_l + distance_r)/2)
        #how fast did the robot move
        #distance / time_needed
        #fitness = fitness #+velocity bonus
        print('fitness:' + str(fitness))
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)
        print('stopped simulation')

        return fitness

    def changeNetworkStep(self):
        self.step = self.step + 1
        for network in self._population:
            network.step = network.step + 1
            if self.step > 1:
                i = 44
                while i < 76:
                    network.weights[i] = 0
                    i = +1
            else:
                i = 84
                while i < 96:
                    network.weights[i] = 0
                    i = +1
                i = 108
                while i < 120:
                    network.weights[i] = 0
                    i = +1


    def getBestNetworks(self):

        bestNetworks = []
        fitnessList = []

        for network in self._population:
            print(self._population.index(network))
            fitness = 0
            for x in range(0, 3):
                fitness = fitness + self.calculateFitness(network)
                network.resetNetwork()
            fitness = fitness / 3
            fitnessList.append(fitness)

        if max(fitnessList) > 1.5 & self.step == 0:
            self.changeNetworkStep()
        elif max(fitnessList) > 2 & self.step == 1:
            self.changeNetworkStep()

        numpyfitness = np.array(fitnessList)
        revindices = np.argsort(numpyfitness)
        indices = np.flipud(revindices)
        meanfitness = np.mean(fitnessList)
        bestIndizes = np.argsort(numpyfitness)[:5]
        bestFitness = []

        for index in indices:
            bestNetworks.append(self._population[index])


        for index in bestIndizes:
            bestFitness.append(self._population[index])
        self.safeFitness(meanfitness, bestFitness)

        return bestNetworks

    def selectOne(self):
        #print('selection')
        maximum = 0
        i = 0
        while i < len(self.ranking):
            maximum = maximum + self.ranking[i]
            i = i + 1
        pick = random.uniform(0, maximum)
        current = 0
        i = 0
        while i < len(self.ranking):
            current += self.ranking[i]
            if current >= pick:
                return i
            i += 1



    # create the next generation
    def createNextGeneration(self, bestNetworks):
        print('Next Generation')
        self._population = []
        bestNetworks[0].resetNetwork()
        bestNetworks[1].resetNetwork()
        self._population.append(bestNetworks[0])
        self._population.append(bestNetworks[1])

        while len(self._population) < self.size_of_population:
            probability = random.randint(0, 100)
            #crossover with probable mutation
            if probability <= self.crossover_rate:
                child_network = self.crossoverNetwork(bestNetworks[self.selectOne()], bestNetworks[self.selectOne()])
                mutate = random.randint(0, 1)
                if mutate == 1:
                    self.createMutantNetwork(child_network)
                    self._population.append(child_network)
                    continue
            else:
                #only mutation
                #print(m)
                #print(len(best5Networks))
                child_network = self.createMutantNetwork(bestNetworks[self.selectOne()])
                self._population.append(child_network)
        #print(self._population)

    def createMutantNetwork(self, network):
        new_weights = []
        for weight in network.weights:
            # probability to mutate into weightmutation
            if random.randint(1, 100) <= self.mutation_rate:
                mutation = random.uniform(-self.factor, self.factor)
                weight = weight + mutation
            new_weights.append(weight)
        child_network = WalkingNetwork.WalkingNetwork(new_weights, self.robot, self.clientID, self.step)
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
        child_network = WalkingNetwork.WalkingNetwork(new_weights, self.robot, self.clientID, self.step)
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
