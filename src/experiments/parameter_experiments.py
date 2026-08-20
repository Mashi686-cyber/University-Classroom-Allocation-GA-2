import csv
import json
import os
from src.genetic_algorithm.genetic_algorithm import GeneticAlgorithm

BASE_PARAMS = {
    "population_size": 50,
    "generations": 100,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "elitism": 2,
    "random_seed": 42
}

def load_dataset(size="small"):
    base_dir = f"data/generated/{size}"
    def load_csv(name):
        with open(f"{base_dir}/{name}", 'r') as f:
            return list(csv.DictReader(f))
    return load_csv("courses.csv"), load_csv("classrooms.csv"), load_csv("timeslots.csv")

def run_experiment_suite(experiment_name, param_name, param_values, dataset="small"):
    courses, classrooms, timeslots = load_dataset(dataset)
    
    results_list = []
    
    for val in param_values:
        config = BASE_PARAMS.copy()
        config[param_name] = val
        
        print(f"Running {experiment_name} | {param_name} = {val} ...")
        
        ga = GeneticAlgorithm(courses, classrooms, timeslots, config=config)
        res = ga.run()
        
        # Calculate mean fitness history
        mean_fitness = sum(res["best_fitness_history"]) / len(res["best_fitness_history"]) if res["best_fitness_history"] else 0
        
        record = {
            "parameter": param_name,
            "value": val,
            "final_fitness": res["final_fitness"],
            "allocated_courses": len([g for g in res["best_chromosome"].genes.values() if g[0] is not None]),
            "unallocated_courses": res["violations"].get("unallocated_courses", 0),
            "classroom_conflicts": res["violations"].get("classroom_conflicts", 0),
            "lecturer_conflicts": res["violations"].get("lecturer_conflicts", 0),
            "student_group_conflicts": res["violations"].get("student_group_conflicts", 0),
            "capacity_violations": res["violations"].get("capacity_violations", 0),
            "facility_violations": res["violations"].get("facility_violations", 0),
            "room_type_violations": res["violations"].get("room_type_violations", 0),
            "availability_violations": res["violations"].get("availability_violations", 0),
            "utilization": res["utilization"],
            "execution_time": res["execution_time_seconds"],
            "best_generation": res["best_generation"],
            "mean_fitness_history": mean_fitness
        }
        results_list.append(record)
        
    # Save to CSV
    os.makedirs("results/experiments", exist_ok=True)
    filename = f"results/experiments/{experiment_name}_results.csv"
    if results_list:
        keys = results_list[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results_list)
            
    print(f"Saved {filename}\n")
    return results_list

def run_all_experiments():
    # 1. Population Size
    run_experiment_suite("population_size", "population_size", [25, 50, 100, 200])
    
    # 2. Generations
    run_experiment_suite("generations", "generations", [50, 100, 200, 500])
    
    # 3. Mutation Rate
    run_experiment_suite("mutation_rate", "mutation_rate", [0.01, 0.05, 0.10, 0.20])
    
    # 4. Crossover Rate
    run_experiment_suite("crossover_rate", "crossover_rate", [0.60, 0.70, 0.80, 0.90])

if __name__ == "__main__":
    run_all_experiments()
