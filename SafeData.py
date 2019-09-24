import csv
from pathlib import Path
import json
from NIPSChallenge.NIPSNetwork import NIPSNetwork

    
def safeMeanAndTopXFitnesses(mean_fitness, best_x_fitnesses):
    path = (getBasePath() / 'fitness.csv').resolve()
    fitness_string = ''
    for fitness in best_x_fitnesses:
        fitness_string += str(fitness) + ' '
    with open(str(path), 'a') as csvfile1:
        errorwriter = csv.writer(csvfile1, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        errorwriter.writerow([str(mean_fitness), fitness_string])


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
    
    with open('office_run.json', 'w') as outfile:
        json.dump(data, outfile)
    print("safed population to json")

    
def loadPopulation():
    population = []
    with open('office_run.json') as json_file:
        data = json.load(json_file)
    for nw in data['networks']:
        population.append(NIPSNetwork(nw['weights']))
    print("loaded population from json")
    return population
