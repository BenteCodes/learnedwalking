import csv

    
def safeMeanAndTop5Fitnesses(self, meanfitness, best5Fitnesses):
    with open('output/fitness.csv', 'a') as csvfile1:
        errorwriter = csv.writer(csvfile1, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        errorwriter.writerow([str(self.current_iteration), str(meanfitness), str(best5Fitnesses[0]), str(best5Fitnesses[1]), str(best5Fitnesses[2]), str(best5Fitnesses[3]), str(best5Fitnesses[4])])


def safeNetwork(self, network):
    with open('output/network.csv', 'wb') as csvfile:
        weightwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        weightstring = []
        for weight in network.weights:weightstring.append(str(weight) + ',')
        weightwriter.writerow(weightstring)
