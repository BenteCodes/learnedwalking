import csv

class SimplePatternGenerator:

    def __init__(self, pattern_name1, pattern_name2, pattern_name3, pattern_name4):
        self.pattern1 = self.getpatternfromdata(pattern_name1)
        self.pattern2 = self.getpatternfromdata(pattern_name2)
        self.pattern3 = self.getpatternfromdata(pattern_name3)
        self.pattern4 = self.getpatternfromdata(pattern_name4)

        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        self.currentstep = 0

    def getpatternfromdata(self, dataname):
        tmparray = []
        with open(dataname, 'r') as csvfile:
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

