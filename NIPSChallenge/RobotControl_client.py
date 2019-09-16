'''
Created on Sep 12, 2019

@author: alica
'''
import opensim as osim  # This error is here because of the virtual env
from osim.http.client import Client  # This error is here because of the virtual env
import numpy as np
from RobotControlAbstract import RobotControlAbstract
import NIPSChallenge.JSONStuff as JSONStuff


class RobotControlNipsClient(RobotControlAbstract):
    
    '''
    Initiates the simulator and the connection
    '''

    def __init__(self):
        # Settings
        self.remote_base = "http://osim-rl-grader.aicrowd.com/"
        self.aicrowd_token = "a66245c8324e2d37b92f098a57ef3f99"  # use your aicrowd token
        # your aicrowd token (API KEY) can be found at your prorfile page at https://www.aicrowd.com

        self.client = Client(self.remote_base)

        # Create environment
        self.observation = self.client.env_create(self.aicrowd_token, env_id='L2M2019Env')
        self.reward = 0

    def startSimulation(self):
        print('start simulation')
        self.reward = 0
        self.observation = self.client.env_reset()

    def stopSimulation(self):
        if self.done:
            print('stopped simulation')

    def robotFell(self):
        return self.done

    def walkRobot(self, motor_values):
        motor_values = JSONStuff.transformActionIntoJSON(motor_values)
        print(type(motor_values))
        [observation, reward, done, info] = self.client.env_step(motor_values)
        self.observation = observation
        self.done = done
        self.reward += reward  # >TODO check if reward is cumulativ on it's own
        print(info)  # TODO what is info/remove
        return np.zeros((16, 1))  # TODO fix once real number is known
        # return self.prepareObersavationForNw(self.observation)

    def getEvalData(self):
        return self.reward  # FIXME this seems to be a tuple?
