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

    def __init__(self, visualization):
        # Create environment
        self.env = L2M2019Env(visualize=visualization)
        self.observation = self.env.reset()
        self.reward = 0

    def startSimulation(self):
        self.reward = 0
        self.observation = self.env.reset()

    def robotFell(self):
        return self.done

    def walkRobot(self, motor_values):
        [observation, reward, done, _info] = self.env.step(motor_values)
        self.observation = observation
        self.done = done
        self.reward += reward  # >TODO check if reward is cumulativ on it's own
       
        # return self.prepareObersavationForNw(self.observation)

    def getEvalData(self):
        return self.reward
