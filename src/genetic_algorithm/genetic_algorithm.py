import copy
import random
import time
import json
import csv

from src.genetic_algorithm.config import GA_PARAMS
from src.genetic_algorithm.chromosome import Chromosome
from src.genetic_algorithm.fitness import FitnessEvaluator
from src.genetic_algorithm.selection import tournament_selection
from src.genetic_algorithm.crossover import uniform_crossover
from src.genetic_algorithm.mutation import mutate

class GeneticAlgorithm:
    def __init__(self, courses, classrooms, timeslots, config=None):
        self.config = config if config else GA_PARAMS
        random.seed(self.config["random_seed"])
        
        self.courses = courses
        self.classrooms = classrooms
        self.timeslots = timeslots
        
        self.evaluator = FitnessEvaluator(courses, classrooms, timeslots)
        
        # Precompute valid timeslot windows
        self.timeslot_windows = {}
        for duration in [1, 2]:
            windows = []
            for i in range(len(self.timeslots)):
                window = [self.timeslots[i]]
                valid = True
                for j in range(1, duration):
                    if i + j >= len(self.timeslots):
                        valid = False
                        break
                    prev_ts = self.timeslots[i + j - 1]
                    curr_ts = self.timeslots[i + j]
                    
                    if prev_ts["Day"] != curr_ts["Day"] or prev_ts["End_Time"] != curr_ts["Start_Time"]:
                        valid = False
                        break
                    window.append(curr_ts)
                if valid:
                    windows.append(",".join([ts["Time_Slot_ID"] for ts in window]))
            self.timeslot_windows[duration] = windows
            
        self.population = []
        self.best_fitness_history = []
        self.best_generation = 0
        
    def init_population(self):
        for _ in range(self.config["population_size"]):
            chrom = Chromosome()
            chrom.randomize(self.courses, self.classrooms, self.timeslot_windows)
            self.population.append(chrom)
            
    def run(self):
        start_time = time.time()
        
        self.init_population()
        
        # Initial evaluation
        for chrom in self.population:
            self.evaluator.evaluate(chrom)
            
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        initial_fitness = self.population[0].fitness
        max_fitness_so_far = initial_fitness
        
        for gen in range(self.config["generations"]):
            new_population = []
            
            # Elitism
            elitism_count = self.config["elitism"]
            for i in range(elitism_count):
                new_population.append(copy.deepcopy(self.population[i]))
                
            # Generate rest of population
            while len(new_population) < self.config["population_size"]:
                parent1 = tournament_selection(self.population)
                parent2 = tournament_selection(self.population)
                
                if random.random() < self.config["crossover_rate"]:
                    child1, child2 = uniform_crossover(parent1, parent2)
                else:
                    child1 = copy.deepcopy(parent1)
                    child2 = copy.deepcopy(parent2)
                    
                mutate(child1, self.config["mutation_rate"], self.courses, self.classrooms, self.timeslot_windows)
                mutate(child2, self.config["mutation_rate"], self.courses, self.classrooms, self.timeslot_windows)
                
                new_population.append(child1)
                if len(new_population) < self.config["population_size"]:
                    new_population.append(child2)
                    
            self.population = new_population
            
            # Evaluate new population
            for chrom in self.population:
                self.evaluator.evaluate(chrom)
                
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            self.best_fitness_history.append(self.population[0].fitness)
            
            if self.population[0].fitness > max_fitness_so_far:
                max_fitness_so_far = self.population[0].fitness
                self.best_generation = gen
            
            # Early stopping check if no hard constraints violated (fitness > 0)
            if self.population[0].fitness > 0:
                print(f"Perfect feasible solution found at generation {gen}!")
                break
                
        exec_time = time.time() - start_time
        best_chrom = self.population[0]
        fitness, violations, util = self.evaluator.evaluate(best_chrom)
        
        return {
            "initial_fitness": initial_fitness,
            "final_fitness": best_chrom.fitness,
            "best_fitness_history": self.best_fitness_history,
            "best_generation": self.best_generation,
            "best_chromosome": best_chrom,
            "violations": violations,
            "utilization": util,
            "execution_time_seconds": exec_time
        }

def run_experiment(size="small"):
    base_dir = f"data/generated/{size}"
    
    def load_csv(name):
        with open(f"{base_dir}/{name}", 'r') as f:
            return list(csv.DictReader(f))
            
    courses = load_csv("courses.csv")
    classrooms = load_csv("classrooms.csv")
    timeslots = load_csv("timeslots.csv")
    
    print(f"Running GA experiment on {size.upper()} dataset...")
    ga = GeneticAlgorithm(courses, classrooms, timeslots)
    result = ga.run()
    
    # Save best allocations
    allocations = result["best_chromosome"].to_allocations(courses)
    if allocations:
        keys = allocations[0].keys()
        with open(f"results/ga/{size}_ga.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(allocations)
            
    # Save summary
    summary = {
        "dataset_size": size,
        "population_size": GA_PARAMS["population_size"],
        "generations": GA_PARAMS["generations"],
        "crossover_rate": GA_PARAMS["crossover_rate"],
        "mutation_rate": GA_PARAMS["mutation_rate"],
        "elitism": GA_PARAMS["elitism"],
        "random_seed": GA_PARAMS["random_seed"],
        "initial_fitness": result["initial_fitness"],
        "final_fitness": result["final_fitness"],
        "best_fitness": max([result["initial_fitness"]] + result["best_fitness_history"]),
        "best_fitness_history": result["best_fitness_history"],
        "allocated_courses": len(allocations),
        "unallocated_courses": result["violations"]["unallocated_courses"],
        "classroom_conflicts": result["violations"]["classroom_conflicts"],
        "lecturer_conflicts": result["violations"]["lecturer_conflicts"],
        "student_group_conflicts": result["violations"]["student_group_conflicts"],
        "capacity_violations": result["violations"]["capacity_violations"],
        "facility_violations": result["violations"]["facility_violations"],
        "room_type_violations": result["violations"]["room_type_violations"],
        "availability_violations": result["violations"]["availability_violations"],
        "utilization": result["utilization"],
        "execution_time_seconds": result["execution_time_seconds"]
    }
    
    with open(f"results/ga/{size}_ga_summary.json", 'w') as f:
        json.dump(summary, f, indent=4)
        
    print("GA execution finished. Summary:")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    run_experiment("small")
