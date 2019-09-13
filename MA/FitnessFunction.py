import math
from FitnessFunctionAbstract import FitnessFunctionAbstract


class FitnessFunction(FitnessFunctionAbstract):
    
    def __init__(self):
        pass

    def getFitness(self, did_fall, position_ref, position_robot_foot_r, position_robot_foot_l):
        fitness = 0
        # fitness += self.penalizeNonMovement(did_move)

        fitness += self.penalizeFalling(did_fall)

        fitness += self.calcDistanceMoved(position_ref, position_robot_foot_r, position_robot_foot_l)
        return fitness
           
    def penalizeFalling(self, did_fall):
        if did_fall:
            return -100  # really don't fall
        return 0

    # def penalizeNonMovement(self, did_move):
        # if not did_move:
        # return -2000  # really, really move

    def calcDistanceMoved(self, pos_start, pos_foot_r, pos_foot_l):
        distance_right_foot = self.calcEuclideanDistance(pos_start, pos_foot_r)
        distance_left_foot = self.calcEuclideanDistance(pos_start, pos_foot_l)
        return (distance_right_foot + distance_left_foot) / 2
    
    def calcEuclideanDistance(self, point1, point2):
        return math.sqrt((math.pow((point1[0] - point2[0]), 2)) + (math.pow((point1[1] - point2[1]), 2)))
    
