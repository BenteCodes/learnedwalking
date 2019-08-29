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
        if network.highest_angle == 0: #if there is 0 movement
            return -2000
        return 0


    def calcDistanceMoved(self, position_ref, position_robot_foot_r, position_robot_foot_l):
        distance_r = math.sqrt((math.pow((position_ref[0] - position_robot_foot_r[0]), 2)) + (math.pow((position_ref[1] - position_robot_foot_r[1]), 2)) + (math.pow((position_ref[2] - position_robot_foot_r[2]), 2)))
        distance_l = math.sqrt((math.pow((position_ref[0] - position_robot_foot_l[0]), 2)) + (math.pow((position_ref[1] - position_robot_foot_l[1]), 2)) + (math.pow((position_ref[2] - position_robot_foot_l[2]), 2)))
        return (distance_l + distance_r) / 2
    