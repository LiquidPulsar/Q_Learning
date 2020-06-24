import random
from functools import reduce

POPULATION_SIZE=8
NUM_OF_ELITE_CHROMOSOMES = 1 #how many wont mutate
TOURNAMENT_SELECTION_SIZE = 4
MUTATION_RATE = 0.25 #probability a chromosome will mutate
TARGET_CHROMOSOME=[random.choice([0,1])for i in range(30)]

class Chromosome():
    def __init__(self): self.genes = [random.choice((0,1))for i in range(len(TARGET_CHROMOSOME))]
    def get_genes(self): return self.genes
    def get_fitness(self): return reduce(lambda x,y: (x+1 if self.genes[y] == TARGET_CHROMOSOME[y] else x), range(len(TARGET_CHROMOSOME)),0) #increase fitness by 1 if mathes the gene in target chromosome, repeat for every gene    
    def __str__(self): return str(self.genes)
    
class Population():
    def __init__(self,size): self._chromosomes = [Chromosome() for _ in range(size)]
    def get_chromosomes(self): return self._chromosomes

class GeneticAlgorithm():
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop))

    @staticmethod
    def _crossover_population(pop):
        crossover_pop=Population(0)
        for i in range(NUM_OF_ELITE_CHROMOSOMES):
            crossover_pop.get_chromosomes().append(pop.get_chromosomes()[i])
        for i in range(NUM_OF_ELITE_CHROMOSOMES,POPULATION_SIZE): #take all chromosomes not elite
            c_1 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
            c_2 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
            crossover_pop.get_chromosomes().append(GeneticAlgorithm._crossover_chromosomes(c_1,c_2))
        return crossover_pop
    
    @staticmethod
    def _mutate_population(pop):
        for i in range(NUM_OF_ELITE_CHROMOSOMES,POPULATION_SIZE): #take all chromosomes not elite
            GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[i])
        return pop

    @staticmethod
    def _crossover_chromosomes(c_1,c_2):
        crossover_chrom = Chromosome()
        for i in range(len(TARGET_CHROMOSOME)):
            crossover_chrom.get_genes()[i]=c_1.get_genes()[i] if random.random() < 0.5 else c_2.get_genes()[i]
        return crossover_chrom

    @staticmethod
    def _mutate_chromosome(chromosome):
        for i in range(len(TARGET_CHROMOSOME)):
            if random.random() < MUTATION_RATE:
                chromosome.get_genes()[i]=1 if random.random() < 0.5 else 0           

    @staticmethod
    def _select_tournament_population(pop):
        tournament_pop = Population(0)
        for i in range(TOURNAMENT_SELECTION_SIZE):
            tournament_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0,POPULATION_SIZE)])
        tournament_pop.get_chromosomes().sort(key=lambda x: x.get_fitness(),reverse=True)
        
        return tournament_pop
    
def _print_population(pop, gen):
    print("\n--------------------------------------")
    print(f"Gen #{gen}, Fittest =",pop.get_chromosomes()[0].get_fitness())
    print("Target chromosome: ",TARGET_CHROMOSOME)
    print("--------------------------------------")
    for number,chromosome in enumerate(pop.get_chromosomes()):
        print(f"Chromosome number {number+1}:{chromosome}¦Fitness: {chromosome.get_fitness()}")
"""
population = Population(POPULATION_SIZE)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(),reverse=True)
_print_population(population,0)
gen_num=1
while population.get_chromosomes()[0].get_fitness()<len(TARGET_CHROMOSOME): #has fittest chromosome reached the max fitness??
    population = GeneticAlgorithm.evolve(population)
    population.get_chromosomes().sort(key=lambda x: x.get_fitness(),reverse=True) #sort the chromosomes by fitness
    _print_population(population,gen_num)
    gen_num+=1
"""
import json
with open("qTable.txt") as file:
    print(json.load(file))