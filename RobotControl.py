

class RobotControl:
      	
 	def __init__(self, robot, clientID, more_motors): 
         self.robot = robot
         self.clientID = clientID
         self.more_motors = more_motors
         


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
      
      
	 def moveRobot(self, motor_values):
	        # generating motor values for the next flag_more_motors
	        if self.more_motors > 0 :
	            full_legs = true
	        
	        self.setRightLeg(motor_values, full_legs)
	        self.setLeftLeg(motor_values, full_legs)
	        
	        if self.more_motors > 1:
	            self.setRightArm(motor_values)
	            self.setLeftArm(motor_values)
	
	        time.sleep(0.01)
 
    def setRightArm(self, motorValues):
        self.robot.changeAngle("r_shoulder_y",  motorValues[(0, 0)], 1)
        self.robot.changeAngle("r_shoulder_z",  motorValues[(0, 1)], 1)
        self.robot.changeAngle("r_arm_x",       motorValues[(0, 2)], 1)
        self.robot.changeAngle("r_elbow_y",     motorValues[(0, 3)], 1)


    def setLeftArm(self, motorValues):
        self.robot.changeAngle("l_shoulder_y",  motorValues[(0, 4)], 1)
        self.robot.changeAngle("l_shoulder_z",  motorValues[(0, 5)], 1)
        self.robot.changeAngle("l_arm_x",       motorValues[(0, 6)], 1)
        self.robot.changeAngle("l_elbow_y",     motorValues[(0, 7)], 1)
      
        
    def setLeftLeg(self, motorValues, all_motors):
        self.robot.changeAngle("l_hip_y",   motorValues[(0, 16)], 1)
        self.robot.changeAngle("l_knee_y",  motorValues[(0, 17)], 1)
        self.robot.changeAngle("l_ankle_y", motorValues[(0, 18)], 1)
                    
        if all_motors:
            self.robot.changeAngle("l_hip_x",   motorValues[(0, 14)], 1)
            self.robot.changeAngle("l_hip_z",   motorValues[(0, 15)], 1)
            self.robot.changeAngle("l_ankle_x", motorValues[(0, 19)], 1)
  
  
    def setRightLeg(self, motorValues, all_motors):
        self.robot.changeAngle("r_hip_y",   motorValues[(0, 10)], 1)
        self.robot.changeAngle("r_knee_y",  motorValues[(0, 11)], 1)
        self.robot.changeAngle("r_ankle_y", motorValues[(0, 12)], 1)
        
        if all_motors:
            self.robot.changeAngle("r_hip_x",   motorValues[(0, 8)], 1)
            self.robot.changeAngle("r_hip_z",   motorValues[(0, 9)], 1)
            self.robot.changeAngle("r_ankle_x", motorValues[(0, 13)], 1)
      
        
    