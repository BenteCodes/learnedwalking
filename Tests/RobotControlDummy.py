# 2 outputneurons try to be as far away from 0 as possbile after the run
from RobotControlAbstract import RobotControlAbstract 

class RobotControlDummy(RobotControlAbstract):
    
    def __init__(self, more_motors):
        self.more_motors = more_motors
      
    def startSimulation(self):
        pass
        
    def stopSimulation(self):
    	pass  

    def robotFell(self):
        return False

    def walkRobot(self, motor_values):
    	self.motor_values = motor_values
		pass
      
    def getEvalData(self):
		return self.robotFell(), 0, self.motor_values[5], self.motor_values[10]        
    