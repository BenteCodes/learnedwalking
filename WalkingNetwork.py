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

    def __init__(self, weights, robot, clientID, step):
        self.weights = weights
        self.last_state_hidden = np.ones((1, 4))
        self.number_of_hidden_units = 4
        self.weights_ih1 = np.matrix(weights[0:10])
        self.weights_ih2 = np.matrix(weights[10:20])
        self.weights_ih3 = np.matrix(weights[20:30])
        self.weights_ih4 = np.matrix(weights[30:40])
        self.weights_hh = np.matrix(weights[40:44])
        self.weights_ho = np.matrix(weights[44:124])
        self.weights_ho = np.reshape(self.weights_ho, (4, 20))
        #self.robot = nicomotion.Motion.Motion("../../../json/nico_humanoid_upper_with_hands_vrep.json",vrep=True)
        #print(self.weights_ho)
        self.simple_pattern = simple_pattern_generator.simplePatternGenerator('sinepattern.csv', 'plussinepattern.csv', 'blopppattern.csv', 'broadsinepattern.csv')
        self.robot = robot
        self.highest_angle = 0
        self.shouldwalk = True
        self.step = step
        self.clientID = clientID


    #collects the Input from various sources
    # todo networks as parameters:  inputnetwork1, inputnetwork2, inputnetwork3, inputnetwork4
    def getInput(self):
        input_matrix = np.zeros((10, 1))
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

        # 4 Basic pattern
        self.simple_pattern.nextStep()
        pattern1 = self.simple_pattern.value1
            #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork1.getOutput()
        np.put(input_matrix, 6, pattern1)
        pattern2 = self.simple_pattern.value2
            #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork2.getOutput()
        np.put(input_matrix, 7, pattern2)
        pattern3 = self.simple_pattern.value3
            #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork3.getOutput()
        np.put(input_matrix, 8, pattern3)
        pattern4 = self.simple_pattern.value4
            #todo wieder einfuegen, wenn pasic pattern_network laeuft: inputnetwork4.getOutput()
        np.put(input_matrix, 9, pattern4)

        return input_matrix

    # forewardprobagation
    # input is a np matrix [10x1]
    def getOutput(self, input_martix):
        hidden = self.number_of_hidden_units
        state_input = input_martix
        while hidden > 1:
            state_input = np.concatenate((state_input, input_martix), axis=1)
            hidden = hidden - 1

        assembled_hidden_input = np.concatenate((state_input, self.last_state_hidden), axis=0)
        #done until here
        assembled_hidden_weights = self.weights_ih1
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.weights_ih2), axis=0)
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.weights_ih3), axis=0)
        assembled_hidden_weights = np.concatenate((assembled_hidden_weights, self.weights_ih4), axis=0)
        assembled_hidden_weights = np.insert(assembled_hidden_weights, [10], np.transpose(self.weights_hh), axis=1)
        state_hidden = (logistic.cdf(np.matrix([np.diagonal(assembled_hidden_weights * assembled_hidden_input, 0)]))+2)-1

        #print(state_hidden)
        state_output = (logistic.cdf(state_hidden * self.weights_ho) * 2) - 1
        #print(state_output)
        self.last_state_hidden = state_hidden

        return state_output

    def moveRobot(self):
        # generating motorvalus for the next step
        motorValues = self.getOutput(self.getInput())

        for value in motorValues[0]:
            self.highest_angle = self.highest_angle + value

        #transferring the motorvalues to the robot (NICO)
        if self.step > 1:
        #r_arm
            self.robot.changeAngle("r_shoulder_y", motorValues[(0, 0)], 1)
            self.robot.changeAngle("r_shoulder_z", motorValues[(0, 1)], 1)
            self.robot.changeAngle("r_arm_x", motorValues[(0, 2)], 1)
            self.robot.changeAngle("r_elbow_y", motorValues[(0, 3)], 1)
        #l_arm
            self.robot.changeAngle("l_shoulder_y", motorValues[(0, 4)], 1)
            self.robot.changeAngle("l_shoulder_z", motorValues[(0, 5)], 1)
            self.robot.changeAngle("l_arm_x", motorValues[(0, 6)], 1)
            self.robot.changeAngle("l_elbow_y", motorValues[(0, 7)], 1)

        if self.step > 0:
            #r_leg_add
            self.robot.changeAngle("r_hip_x", motorValues[(0, 8)], 1)
            self.robot.changeAngle("r_hip_z", motorValues[(0, 9)], 1)
            self.robot.changeAngle("r_ankle_x", motorValues[(0, 13)], 1)
            #l_leg_add
            self.robot.changeAngle("l_hip_x", motorValues[(0, 14)], 1)
            self.robot.changeAngle("l_hip_z", motorValues[(0, 15)], 1)
            self.robot.changeAngle("l_ankle_x", motorValues[(0, 19)], 1)

        #r_leg_always
        self.robot.changeAngle("r_hip_y", motorValues[(0, 10)], 1)
        self.robot.changeAngle("r_knee_y", motorValues[(0, 11)], 1)
        self.robot.changeAngle("r_ankle_y", motorValues[(0, 12)], 1)
        #l_leg_always
        self.robot.changeAngle("l_hip_y", motorValues[(0, 16)], 1)
        self.robot.changeAngle("l_knee_y", motorValues[(0, 17)], 1)
        self.robot.changeAngle("l_ankle_y", motorValues[(0, 18)], 1)
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
