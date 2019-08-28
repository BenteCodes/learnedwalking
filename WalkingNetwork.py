# Imports und so
import numpy as np
from scipy.stats import logistic
import Network
import random
#from nicomotion import Motion
import simple_pattern_generator
import time
import vrep
from RobotControl import RobotControl

# class for that network
# parameters: weights
class WalkingNetwork:
    
    number_of_input_units = 10 #min 4
    number_of_hidden_units = 4
    number_of_output_units = 20
    number_of_weights = (number_of_input_units * number_of_hidden_units) + number_of_hidden_units + (number_of_hidden_units * number_of_output_units)
    number_of_basic_pattern = 4

    # @input weights weights of the network
    # @input robot model of the simulated robot
    # @input clientID ID of the simulator
    # @inout more_motors value of 0,1,2, different number of motors are active TODO
    def __init__(self, weights, robot, clientID, more_motors): 
        checkParameter(weights, more_motors)    
        initNetwork(weights)
        #self.robot = nicomotion.Motion.Motion("../../../json/nico_humanoid_upper_with_hands_vrep.json",vrep=True)
        #print(self.hidden_to_output_all)
        initInputPattern()
        
        initRobotControl(robot, clientID, more_motors)
        
        #self.shouldwalk = True
    
    
    def checkParameters(self, weights, more_motors):
        if not(len(weights) == self.number_of_weights):
            print("Paramcheck: Weights of incorrect number_of_weights")
            
        if not((-1 < more_motors) and (more_motors < 3)):
            print("Paramcheck: Wrong motor number, only 0,1,2 allowed")
        
            
    # disects the weights into the corresponding network parts 
    # 10input -> 4 hidden with recurrant -> 20 output   
    def initNetwork(self, weights):
        self.last_state_hidden = np.ones((1, number_of_hidden_units)) #last states values need to be known for the algo and are 1 at the first run.
        
        position_start = 0
        position_end = number_of_input_units * number_of_hidden_units
        self.input_to_hidden_all = np.matrix(weights[position_start:position_end])
        self.input_to_hidden_all = np.reshape(self.hidden_to_output_all, (number_of_input_units, number_of_hidden_units))

        position_start = position_end
        position_end += number_of_hidden_units        
        self.hidden_to_hidden = np.matrix(weights[position_start:position_end])

        position_start = position_end
        position_end += (number_of_hidden_units * number_of_output_units)         
        self.hidden_to_output_all = np.matrix(weights[position_start:position_end])
        self.hidden_to_output_all = np.reshape(self.hidden_to_output_all, (number_of_hidden_units, number_of_output_units)) #sort after connection not just a long list
    
    def initInputPattern(self):
        self.simple_pattern = simple_pattern_generator.simplePatternGenerator('sinepattern.csv', 'plussinepattern.csv', 'blopppattern.csv', 'broadsinepattern.csv')    
        
    def initRobotControl(self, robot, clientID, more_motors):
            self.robot_control = RobotControl(robot, clientID, more_motors) 
    
    # need to be a 10x1 matrix for matrix purpises, though only 5 get used
    def getInput(self):
        input_matrix = np.zeros((number_of_input_units, 1))

        input_matrix = self.getInputFromSimplePattern(input_matrix, np)

        return input_matrix

    
    def getInputFromSimplePattern(self, input_matrix, np):
        self.simple_pattern.nextStep()
        
        for index in range(number_of_basic_pattern):
            np.put(input_matrix, index, self.simple_pattern[index])
        
        return input_matrix


    # forewardprobagation
    # input is a np matrix [10x1]
    def computeOneStepOnNw(self, state_input):
        hidden = number_of_hidden_units
        while hidden > 1:
            state_input = np.concatenate((state_input, input_martix), axis=1)
            hidden -=  1

        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        #done until here
        assembled_hidden_weights = input_to_hidden_all
        assembled_hidden_weights = np.insert(assembled_hidden_weights, [number_of_input_units], np.transpose(self.hidden_to_hidden), axis=1)
        state_hidden = (logistic.cdf(np.matrix([np.diagonal(assembled_hidden_weights * assembled_hidden_input, 0)]))+2)-1 # TODO check this please, wtf + names!!

        #print(state_hidden)
        state_output = (logistic.cdf(state_hidden * self.hidden_to_output_all) * 2) - 1
        #print(state_output)
        self.last_state_hidden = state_hidden

        return state_output


    #walks in Simulator in scene XY
    # todo implement better stopvalue
    def walkInSimulator(self):
        #while self.shouldwalk:
        while True:
            motor_values = self.computeOneStepOnNw(self.getInput())
            self.robot_control.moveRobot(motor_values)


    def resetHiddenLayer(self):
        self.last_state_hidden = np.ones((1, 4))
    
    def newNWWithDifferentWeights(self, weights):
        return WalkingNetwork(weights, self.robot_control.robot, self.robot_control.clientID, self.robot_control.more_motors)
    
    def getWeights(self):
        return self.weights
    
    def getNumberOfWeights(self):
        return self.number_of_weights
