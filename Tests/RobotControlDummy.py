# 2 outputneurons try to be as far away from 0 as possbile after the run
from RobotControlAbstract import RobotControlAbstract 


class RobotControlDummy(RobotControlAbstract):
    
    def __init__(self):
        self.more_motors = 0  # default
      
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
        return self.robotFell(), [0, 0], [0, self.motor_values[0][5]], [0, self.motor_values[0][10]]        
    
    # TODO this is dirty!
    def setMotorFlag(self, more_motors):
        self.more_motors = more_motors

