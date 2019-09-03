from abc import ABC, abstractmethod


class RobotControlAbstract(ABC):

	@abstractmethod
	def __init__(self, more_motors):
		pass
	
	@abstractmethod
	def startSimulation(self):
		pass  
	
	@abstractmethod
	def stopSimulation(self):
		pass
	
	@abstractmethod
	def robotFell(self):
		pass
	
	@abstractmethod
	def walkRobot(self, motor_values):
		pass

	@abstractmethod
	def getEvalData(self):
		pass
