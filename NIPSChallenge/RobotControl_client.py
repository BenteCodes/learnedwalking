'''
Created on Sep 12, 2019

@author: alica
'''
import opensim as osim  # This error is here because of the virtual env
from osim.http.client import Client  # This error is here because of the virtual env
from NIPSChallenge.RobotControl_local import RobotControlNipsLocal


class RobotControlNipsClient(RobotControlNipsLocal):
    
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

