from MA import vrep
# from nicomotion import Motion
import time
from RobotControlAbstract import RobotControlAbstract 


class RobotControl(RobotControlAbstract):
    robot_string = "../json/nico_humanoid_full_with_grippers_unchecked.json"
    oneshot = ""  # vrep.simx_opmode_oneshot
    oneshot_wait = ""  # vrep.simx_opmode_oneshot_wait
    
    def __init__(self):
        self.more_motors = 0
        # self.robot = Motion.Motion(self.robot_string, vrep=True, vrepHost='127.0.0.1', vrepPort=19997)
        vrep.simxFinish(-1)  # TODO explain why this is here
        self.clientID = vrep.simxStart('127.0.0.1', 19996, True, True, 5000, 5)
        
    # TODO this is dirty!
    def setMotorFlag(self, more_motors):
        self.more_motors = more_motors
      
    def startSimulation(self):
        time.sleep(0.5)
        vrep.simxStartSimulation(self.clientID, self.oneshot)
        time.sleep(0.5)   
        
    def stopSimulation(self):
        return vrep.simxStopSimulation(self.clientID, self.oneshot)

    def robotFell(self):
        torso_handle = vrep.simxGetObjectHandle(self.clientID, "torso_11_visual", self.oneshot_wait)
        [_m, position_robot] = vrep.simxGetObjectPosition(self.clientID, torso_handle[1], -1, self.oneshot_wait)
        return position_robot[2] < 0.2

    def walkRobot(self, motor_values):
        self.controlMotors(motor_values)

    def controlMotors(self, motor_values):
        if self.more_motors > 0:
            full_legs = True
        self.setLeftLeg(motor_values, full_legs)
        self.setRightLeg(motor_values, full_legs)

        if self.more_motors > 1:
            self.setRightArm(motor_values)
            self.setLeftArm(motor_values)
         
        time.sleep(0.01)
 
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
        
    def setLeftLegVertical(self, motorValues):
        self.robot.changeAngle("l_hip_x", motorValues[(0, 14)], 1)
        self.robot.changeAngle("l_hip_z", motorValues[(0, 15)], 1)
        self.robot.changeAngle("l_ankle_x", motorValues[(0, 19)], 1)

    def setLeftLegHorizontal(self, motorValues):
        self.robot.changeAngle("l_hip_y", motorValues[(0, 16)], 1)
        self.robot.changeAngle("l_knee_y", motorValues[(0, 17)], 1)
        self.robot.changeAngle("l_ankle_y", motorValues[(0, 18)], 1)

    def setLeftLeg(self, motorValues, all_motors):
        self.setLeftLegHorizontal(motorValues)                    
        if all_motors:
            self.setLeftLegVertical(motorValues)

    def setRightLegVertical(self, motorValues):
        self.robot.changeAngle("r_hip_x", motorValues[(0, 8)], 1)
        self.robot.changeAngle("r_hip_z", motorValues[(0, 9)], 1)
        self.robot.changeAngle("r_ankle_x", motorValues[(0, 13)], 1)

    def setRightLegHorizontal(self, motorValues):
        self.robot.changeAngle("r_hip_y", motorValues[(0, 10)], 1)
        self.robot.changeAngle("r_knee_y", motorValues[(0, 11)], 1)
        self.robot.changeAngle("r_ankle_y", motorValues[(0, 12)], 1)

    def setRightLeg(self, motorValues, all_motors):
        self.setRightLegHorizontal(motorValues)       
        if all_motors:
            self.setRightLegVertical(motorValues)
      
    def getEvalData(self):
        cube_handle = vrep.simxGetObjectHandle(self.clientID, "reference_cube", self.oneshot_wait)
        [_m, position_ref] = vrep.simxGetObjectPosition(self.clientID, cube_handle[1], -1, self.oneshot_wait)  # print(position_ref)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "right_foot_11_respondable", self.oneshot_wait)
        [_m, position_robot_foot_r] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, self.oneshot_wait)
        foot_handle = vrep.simxGetObjectHandle(self.clientID, "left_foot_11_respondable", self.oneshot_wait)
        [_m, position_robot_foot_l] = vrep.simxGetObjectPosition(self.clientID, foot_handle[1], -1, self.oneshot_wait)  # print(position_robot_foot)
        return self.robotFell(), position_ref, position_robot_foot_r, position_robot_foot_l      
    
