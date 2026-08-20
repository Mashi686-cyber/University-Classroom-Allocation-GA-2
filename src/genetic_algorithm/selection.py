import random

def tournament_selection(population, k=3):
    """
    Selects k individuals randomly from the population and returns the one with the best fitness.
    """
    tournament = random.sample(population, k)
    best = max(tournament, key=lambda chrom: chrom.fitness)
    return best
