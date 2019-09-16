import csv
from pathlib import Path
import json
from NIPSChallenge.NIPSNetwork import NIPSNetwork

    
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


def safePopulation(pop):
    data = {} 
    data['networks'] = []
    for nw in pop:
        data['networks'].append({
            'weights': nw.weights,
            })
    
    with open('data_file.json', 'w') as outfile:
        json.dump(data, outfile)
    print("safed population to json")

    
def loadPopulation():
    population = []
    with open('data_file.json') as json_file:
        data = json.load(json_file)
    for nw in data['networks']:
        population.append(NIPSNetwork(nw['weights']))
    print("loaded population to json")
    return population
