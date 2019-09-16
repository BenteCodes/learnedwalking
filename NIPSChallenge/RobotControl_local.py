'''
Created on Sep 16, 2019

@author: alica
'''
import opensim as osim  # This error is here because of the virtual env
from osim.env import L2M2019Env  # This error is here because of the virtual env
import numpy as np
from RobotControlAbstract import RobotControlAbstract


class RobotControlNipsLocal(RobotControlAbstract):
    
    '''
    Initiates the simulator and the connection
    '''

    def __init__(self):
        
        # Create environment
        self.env = L2M2019Env(visualize=True)
        self.observation = self.env.reset()
        self.reward = 0

    def startSimulation(self):
        print('start simulation')
        self.reward = 0
        self.observation = self.env.reset()

    def stopSimulation(self):
        if self.done:
            print('stopped simulation')

    def robotFell(self):
        return False

    def walkRobot(self, motor_values):
        [observation, reward, done, info] = self.env.step(motor_values[0])
        self.observation = observation
        self.done = done
        self.reward += reward  # >TODO check if reward is cumulativ on it's own  # TODO what is info/remove
        return np.zeros((16, 1))  # TODO fix once real number is known
        # return self.prepareObersavationForNw(self.observation)

    def getEvalData(self):
        return self.reward  # FIXME this seems to be a tuple?
