import math

class FitnessFunction:
    
    def __init__(self):
        pass

    def getFitness(self, network, position_robot, position_ref, position_robot_foot_r, position_robot_foot_l):
        fitness = 0
        fitness += self.penalizeNonMovement(network)

        fitness += self.penalizeFalling(position_robot)

        fitness += self.calcDistanceMoved(position_ref, position_robot_foot_r, position_robot_foot_l)
        return fitness
        
           
    def penalizeFalling(self, position_robot):
        if position_robot[2] < 0.4: # robotFellDownThreshold
            return -100 #relly don't fall
        return 0


    def penalizeNonMovement(self, network):
        if not network.getMovement(): #if there is 0 movement
            return -2000
        return 0


    def calcDistanceMoved(self, pos_start, pos_foot_r, pos_foot_l):
        distance_right_foot = self.calcEuclideanDistance(pos_start, pos_foot_r)
        distance_left_foot = self.calcEuclideanDistance(pos_start, pos_foot_l)
        return (distance_right_foot + distance_left_foot) / 2
    
    
    def calcEuclideanDistance(self, point1, point2):
        return math.sqrt((math.pow((point1[0] - point2[0]), 2)) + (math.pow((point1[1] - point2[1]), 2)))
    