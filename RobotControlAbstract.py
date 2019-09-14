from abc import abstractmethod, ABC


class RobotControlAbstract(ABC):

	@abstractmethod
	def __init__(self):
		pass
	
	@abstractmethod
	def startSimulation(self):
		return NotImplementedError  
	
	@abstractmethod
	def stopSimulation(self):
		return NotImplementedError
	
	@abstractmethod
	def robotFell(self):
		return NotImplementedError
	
	@abstractmethod
	def walkRobot(self, motor_values):
		return NotImplementedError

	@abstractmethod
	def getEvalData(self):
		return NotImplementedError
