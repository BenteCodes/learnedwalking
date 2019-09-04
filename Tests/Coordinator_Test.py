import pytest
from Network import Network
from Tests.RobotControlDummy import RobotControlDummy
from Coordinator import Coordinator


def test_initNetwork():
    cord = Coordinator(20, 50, 50, 20, 0)
    pass


# THIS IS NOT A UNIT TEST!!! ONLY MANUAL EXECUTION
def fullRun():
    cord = Coordinator(20, 50, 50, 20, 0)
    cord.evolve()


fullRun()
