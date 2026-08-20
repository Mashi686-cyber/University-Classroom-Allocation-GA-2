import random
import copy
from src.genetic_algorithm.chromosome import Chromosome

def uniform_crossover(parent1, parent2):
    """
    Performs uniform crossover.
    Iterates through each course and randomly picks the gene from either parent1 or parent2.
    """
    child1_genes = {}
    child2_genes = {}
    
    for c_id in parent1.genes:
        if random.random() < 0.5:
            child1_genes[c_id] = copy.deepcopy(parent1.genes[c_id])
            child2_genes[c_id] = copy.deepcopy(parent2.genes[c_id])
        else:
            child1_genes[c_id] = copy.deepcopy(parent2.genes[c_id])
            child2_genes[c_id] = copy.deepcopy(parent1.genes[c_id])
            
    return Chromosome(child1_genes), Chromosome(child2_genes)
