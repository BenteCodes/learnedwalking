import csv
from pathlib import Path

    
def safeMeanAndTop5Fitnesses(mean_fitness, best_5_fitnesses):
    path = (getBasePath() / 'fitness.csv').resolve()
    with open(str(path), 'a') as csvfile1:
        errorwriter = csv.writer(csvfile1, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        errorwriter.writerow([str(mean_fitness), str(best_5_fitnesses[0]), str(best_5_fitnesses[1]), str(best_5_fitnesses[2]), str(best_5_fitnesses[3]), str(best_5_fitnesses[4])])


def safeNetwork(best_network):
    path = (getBasePath() / 'best_network.csv').resolve()
    with open(str(path), 'w+') as csvfile:
        weightwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        weightstring = []
        for weight in best_network.weights:weightstring.append(str(weight) + ',')
        weightwriter.writerow(weightstring)


def getBasePath():
    base_path = Path(__file__).parent
    base_path = (base_path / 'output/').resolve()
    return base_path
