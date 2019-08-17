# Imports und so
import numpy as np
from scipy.stats import logistic
import Network
import random
#from nicomotion import Motion
import simple_pattern_generator
import time
import vrep

# class for that network
# parameters: weights
class WalkingNetwork:
    
    number_of_inputN = 10
    number_of_hidden_units = 4
    number_of_output_units = 20

    # @input weights weights of the network
    # @input robot model of the simulated robot
    # @input clientID ID of the simulator
    # @inout more_motors value of 0,1,2, different number of motors are active TODO
    def __init__(self, weights, robot, clientID, more_motors):     
        initNetwork(weights)
        #self.robot = nicomotion.Motion.Motion("../../../json/nico_humanoid_upper_with_hands_vrep.json",vrep=True)
        #print(self.hidden_to_output_all)
        initInputPattern()
        
        self.robot = robot
        self.clientID = clientID
        self.flag_more_motors = more_motors
        
        self.shouldwalk = True
        
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
        
        
    #collects the Input from various sources
    # todo networks as parameters:  inputnetwork1, inputnetwork2, inputnetwork3, inputnetwork4

    def getInputFromSimplePattern(self, input_matrix, np):
        self.simple_pattern.nextStep()
        pattern1 = self.simple_pattern.value1 #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork1.getOutput()
        np.put(input_matrix, 6, pattern1)
        pattern2 = self.simple_pattern.value2 #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork2.getOutput()
        np.put(input_matrix, 7, pattern2)
        pattern3 = self.simple_pattern.value3 #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork3.getOutput()
        np.put(input_matrix, 8, pattern3)
        pattern4 = self.simple_pattern.value4 #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork4.getOutput()
        np.put(input_matrix, 9, pattern4)


    def getInputFromIMU(self):
        #Gyro in the 3 axis
        #[m, gyrox] = vrep.simxGetFloatSignal(self.clientID, "gyrox", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 1, gyrox)
        #[m, gyroy] = vrep.simxGetFloatSignal(self.clientID, "gyroy", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 2, gyroy)
        #[m, gyroz] = vrep.simxGetFloatSignal(self.clientID, "gyroz", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 3, gyroz)

        #Accel in the 3 axis
        #[n, accelx] = vrep.simxGetFloatSignal(self.clientID, "accelz", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 4, accelx)
        #[n, accely] = vrep.simxGetFloatSignal(self.clientID, "accelz", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 5, accely)
        #[n, accelz] = vrep.simxGetFloatSignal(self.clientID, "accelz", vrep.simx_opmode_oneshot_wait)
        #np.put(input_matrix, 6, accelz)
        pass

    def getInput(self):
        input_matrix = np.zeros((10, 1))
        self.getInputFromIMU()

        # 4 Basic pattern
        self.getInputFromSimplePattern(input_matrix, np)

        return input_matrix

    # forewardprobagation
    # input is a np matrix [10x1]
    def getOutput(self, input_martix):
        hidden = number_of_hidden_units
        state_input = input_martix
        while hidden > 1:
            state_input = np.concatenate((state_input, input_martix), axis=1)
            hidden = hidden - 1

        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        #done until here
        assembled_hidden_weights = self.input_first_hidden_neuron
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.input_snd_hidden_neuron), axis=0)
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.input_third_hidden_neuron), axis=0)
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.input_fourth_hidden_neuron), axis=0)
        assembled_hidden_weights = np.insert(assembled_hidden_weights, [10], np.transpose(self.hidden_to_hidden), axis=1)
        state_hidden = (logistic.cdf(np.matrix([np.diagonal(assembled_hidden_weights * assembled_hidden_input, 0)]))+2)-1

        #print(state_hidden)
        state_output = (logistic.cdf(state_hidden * self.hidden_to_output_all) * 2) - 1
        #print(state_output)
        self.last_state_hidden = state_hidden

        return state_output


    def setRightArm(self, motorValues):
        self.robot.changeAngle("r_shoulder_y", motorValues[(0, 0)], 1)
        self.robot.changeAngle("r_shoulder_z", motorValues[(0, 1)], 1)
        self.robot.changeAngle("r_arm_x", motorValues[(0, 2)], 1)
        self.robot.changeAngle("r_elbow_y", motorValues[(0, 3)], 1)


    def setLeftArm(self, motorValues):
        self.robot.changeAngle("l_shoulder_y", motorValues[(0, 4)], 1)
        self.robot.changeAngle("l_shoulder_z", motorValues[(0, 5)], 1)
        self.robot.changeAngle("l_arm_x", motorValues[(0, 6)], 1)
        self.robot.changeAngle("l_elbow_y", motorValues[(0, 7)], 1)
        
    def setLeftLeg(self, motorValues):
        if self.flag_more_motors > 0:
            self.robot.changeAngle("l_hip_x", motorValues[(0, 14)], 1)
            self.robot.changeAngle("l_hip_z", motorValues[(0, 15)], 1)
            self.robot.changeAngle("l_ankle_x", motorValues[(0, 19)], 1)

        self.robot.changeAngle("l_hip_y", motorValues[(0, 16)], 1)
        self.robot.changeAngle("l_knee_y", motorValues[(0, 17)], 1)
        self.robot.changeAngle("l_ankle_y", motorValues[(0, 18)], 1)

        
    def setRightLeg(self, motorValues):
        if self.flag_more_motors > 0:
            self.robot.changeAngle("r_hip_x", motorValues[(0, 8)], 1)
            self.robot.changeAngle("r_hip_z", motorValues[(0, 9)], 1)
            self.robot.changeAngle("r_ankle_x", motorValues[(0, 13)], 1)

        self.robot.changeAngle("r_hip_y", motorValues[(0, 10)], 1)
        self.robot.changeAngle("r_knee_y", motorValues[(0, 11)], 1)
        self.robot.changeAngle("r_ankle_y", motorValues[(0, 12)], 1)
        
    def moveRobot(self):
        # generating motor values for the next flag_more_motors
        motorValues = self.getOutput(self.getInput())

        #transferring the motor values to the robot (NICO)
        if self.flag_more_motors > 1:
            self.setRightArm(motorValues)
            self.setLeftArm(motorValues)

        self.setRightLeg(motorValues)
        self.setLeftLeg(motorValues)
       
        return motorValues
        time.sleep(0.01)


    #walks in Simulator in scene XY
    def walkInSimulator(self):
        #open scene

        #let the robot walk
        # todo implement usefull stopvalue
        while True:
            self.moveRobot()


    #walks on the real NICO-robot
    def walkRobot(self):
        i = 0
        while i < 400:
            self.moveRobot()
            torso_handle = vrep.simxGetObjectHandle(self.clientID, "torso_11_visual", vrep.simx_opmode_oneshot_wait)
            [m, position_robot] = vrep.simxGetObjectPosition(self.clientID, torso_handle[1], -1, vrep.simx_opmode_oneshot_wait)
            if position_robot[2] < 0.2:
                break
            #print('walking' + str(i))
            i = i + 1
        #print('finished moving')

    def resetNetwork(self):
        self.last_state_hidden = np.ones((1, 4))

#weigts1 = [random.randint(-5,5) for _ in range(12)]
#weigts2 = [random.randint(-5,5) for _ in range(12)]
#weigts3 = [random.randint(-5,5) for _ in range(12)]
#weigts4 = [random.randint(-5,5) for _ in range(12)]
#bpn1 = Network.BasicPGN(weigts1, 1, 2)
#bpn2 = Network.BasicPGN(weigts2, 1, 2)
#bpn3 = Network.BasicPGN(weigts3, 1, 2)
#bpn4 = Network.BasicPGN(weigts4, 1, 2)
#mylist = [random.uniform(-5, 5) for _ in range(124)]
#print(len(mylist))
#robot = Motion.Motion("../json/nico_humanoid_full_with_grippers_unchecked.json", vrep=True, vrepHost='127.0.0.1', vrepPort=19997)
#testgait = WalkingNetwork(mylist, robot)
#testgait.walkRobot()
