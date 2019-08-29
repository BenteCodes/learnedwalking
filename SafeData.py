
    
def safeFitness(self, meanfitness, best5Fitness):
    with open('fitnessmoremotors_static.csv', 'a') as csvfile1:
        errorwriter = csv.writer(csvfile1, delimiter=' ',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)

        errorwriter.writerow([str(self.current_iteration), str(meanfitness), str(best5Fitness[0]), str(best5Fitness[1]), str(best5Fitness[2]), str(best5Fitness[3]), str(best5Fitness[4])])

def safeNetwork(self, network):
    with open('networkmoremotors_static.csv', 'wb') as csvfile:
        weightwriter = csv.writer(csvfile, delimiter=' ',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        weightstring = []
        for weight in network.weights:
             weightstring.append(str(weight) + ',')
        weightwriter.writerow(weightstring)
