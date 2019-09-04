import csv
from pathlib import Path


class SimplePatternGenerator:

    base_path = Path(__file__).parent
    base_path = (base_path / 'csv/').resolve()
    path1 = (base_path / 'sinepattern.csv').resolve()
    path2 = (base_path / 'plussinepattern.csv').resolve()
    path3 = (base_path / 'blopppattern.csv').resolve()
    path4 = (base_path / 'broadsinepattern.csv').resolve()

    def __init__(self):
        self.pattern1 = self.getPatternFromPath(self.path1)
        self.pattern2 = self.getPatternFromPath(self.path2)
        self.pattern3 = self.getPatternFromPath(self.path3)
        self.pattern4 = self.getPatternFromPath(self.path4)

        self.value1 = 0 
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        self.currentstep = 0

    def getPatternFromPath(self, path):
        tmparray = []
        with open(path, 'r') as csvfile:
            patternreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in patternreader:
                tmparray.append(float(row[1]))
        return tmparray

    def nextStep(self):
        self.currentstep = self.currentstep + 4
        if self.currentstep >= 100:
            self.currentstep = 0
        self.value1 = self.pattern1[self.currentstep]
        self.value2 = self.pattern2[self.currentstep]
        self.value3 = self.pattern3[self.currentstep]
        self.value4 = self.pattern4[self.currentstep]
        return [self.value1, self.value2, self.value3, self.value4]

    def getNumberOfPatterns(self):
        return 4
