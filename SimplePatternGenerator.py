import csv
from pathlib import Path


class SimplePatternGenerator:

    base_path = Path(__file__).parent
    base_path = (base_path / 'csv/').resolve()
    path1 = (base_path / 'sinepattern.csv').resolve()
    path2 = (base_path / 'plussinepattern.csv').resolve()
    path3 = (base_path / 'blopppattern.csv').resolve()
    path4 = (base_path / 'broadsinepattern.csv').resolve()

    number_of_patterns = 4
    step_length = 1
    phase = 100

    def __init__(self):
        self.pattern = [self.getPatternFromPath(self.path1),
                        self.getPatternFromPath(self.path2),
                        self.getPatternFromPath(self.path3),
                        self.getPatternFromPath(self.path4)]

        self.values = [0, 0, 0, 0]
        self.currentstep = 0
        
    def getPatternFromPath(self, path):
        tmparray = []
        with open(str(path), 'r') as csvfile:
            patternreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in patternreader:
                tmparray.append(float(row[1]))
        return tmparray

    def nextStep(self):
        self.currentstep += self.step_length
        self._handleOverflow()

        for index in range(0, self.number_of_patterns):
            self.values[index] = self.pattern[index][self.currentstep]
            
        return self.values

    def getNumberOfPatterns(self):
        return self.number_of_patterns
    
    def _handleOverflow(self):
        if self.currentstep >= self.phase:
            self.currentstep -= self.phase
            
    def increasePhaseByPI(self):
        self.currentstep += (self.phase / 2)
        self._handleOverflow()
        
