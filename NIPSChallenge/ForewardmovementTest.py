'''
Created on Sep 19, 2019

@author: alica
'''
import numpy as np
from NIPSChallenge.RobotControl_local import RobotControlNipsLocal

bend_knee_action = [1, 1, 0, 0, 0.5, 0, 0, 0, 0, 0, 0.5,  # left leg
                    0, 0, 1, 0, 0, 0.5, 0, 0, 0, 0, 0.5]
make_step_action = [1, 1, 1, 0, 0, 1, 1, 0.5, 0.5, 0.5, 1,  # left leg
                    0, 0, 0.5, 0, 0, 0, 0, 1, 0.5, 0, 0]
make_step_action2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1,  # left leg
                    0, 0, 0.5, 0, 0, 0.5, 0, 0.5, 0, 0, 0]
foot_down_action = [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,  # left leg
                    0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0.5]
bentes_robotcontroll = RobotControlNipsLocal(True)
counter = 0
while True:
    if counter < 20:
        bentes_robotcontroll.walkRobot(np.array([bend_knee_action]))
    counter += 1
    print(counter)
print(bentes_robotcontroll.reward)
