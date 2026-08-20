import csv
import json
import os
import time
import random
import statistics
from collections import defaultdict
from src.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from src.baseline.baseline_allocator import BaselineAllocator
from src.evaluation.constraint_checker import ConstraintChecker
from src.evaluation.metrics import MetricsCalculator

# Fixed GA Configuration
GA_CONFIG = {
    "population_size": 50,
    "generations": 50,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "elitism": 2,
    "random_seed": 42
}

DATASETS = ["small", "medium", "large"]
SEEDS = [42, 43, 44, 45, 46]

def load_dataset(size):
    base_dir = f"data/generated/{size}"
    def load_csv(name):
        with open(f"{base_dir}/{name}", 'r') as f:
            return list(csv.DictReader(f))
    return load_csv("courses.csv"), load_csv("classrooms.csv"), load_csv("timeslots.csv")

def evaluate_baseline(courses, classrooms, timeslots):
    start_time = time.time()
    allocator = BaselineAllocator(courses, classrooms, timeslots)
    allocations = allocator.allocate()
    exec_time = time.time() - start_time
    
    checker = ConstraintChecker(courses, classrooms, timeslots)
    violations = checker.evaluate(allocations)
    
    metrics_calc = MetricsCalculator(classrooms)
    util, _ = metrics_calc.calculate_utilization(allocations)
    
    return {
        "dataset_size": None, # Set later
        "algorithm": "Baseline",
        "seed": "42 (Deterministic)",
        "total_courses": len(courses),
        "allocated_courses": len(allocations),
        "unallocated_courses": violations["unallocated_courses"],
        "classroom_conflicts": violations["classroom_conflicts"],
        "lecturer_conflicts": violations["lecturer_conflicts"],
        "student_group_conflicts": violations["student_group_conflicts"],
        "capacity_violations": violations["capacity_violations"],
        "facility_violations": violations["facility_violations"],
        "room_type_violations": violations["room_type_violations"],
        "availability_violations": violations["availability_violations"],
        "utilization": util,
        "fitness": None, # Baseline has no fitness score
        "execution_time": exec_time
    }

def run_main_experiments():
    all_runs = []
    
    for size in DATASETS:
        print(f"--- Processing Dataset: {size.upper()} ---")
        courses, classrooms, timeslots = load_dataset(size)
        
        # 1. Run Baseline
        print("Running Baseline...")
        baseline_res = evaluate_baseline(courses, classrooms, timeslots)
        baseline_res["dataset_size"] = size.capitalize()
        all_runs.append(baseline_res)
        
        # 2. Run GA for 5 seeds
        for seed in SEEDS:
            print(f"Running GA (Seed {seed})...")
            config = GA_CONFIG.copy()
            config["random_seed"] = seed
            
            ga = GeneticAlgorithm(courses, classrooms, timeslots, config=config)
            res = ga.run()
            
            all_runs.append({
                "dataset_size": size.capitalize(),
                "algorithm": "GA",
                "seed": seed,
                "total_courses": len(courses),
                "allocated_courses": len([g for g in res["best_chromosome"].genes.values() if g[0] is not None]),
                "unallocated_courses": res["violations"]["unallocated_courses"],
                "classroom_conflicts": res["violations"]["classroom_conflicts"],
                "lecturer_conflicts": res["violations"]["lecturer_conflicts"],
                "student_group_conflicts": res["violations"]["student_group_conflicts"],
                "capacity_violations": res["violations"]["capacity_violations"],
                "facility_violations": res["violations"]["facility_violations"],
                "room_type_violations": res["violations"]["room_type_violations"],
                "availability_violations": res["violations"]["availability_violations"],
                "utilization": res["utilization"],
                "fitness": res["final_fitness"],
                "execution_time": res["execution_time_seconds"]
            })
            
    # Save all runs
    os.makedirs("results/comparison", exist_ok=True)
    with open("results/comparison/all_runs.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_runs[0].keys())
        writer.writeheader()
        writer.writerows(all_runs)
        
    # Calculate Statistics & Summary
    summary = []
    stats = []
    
    for size in DATASETS:
        ds_cap = size.capitalize()
        
        baseline_run = [r for r in all_runs if r["algorithm"] == "Baseline" and r["dataset_size"] == ds_cap][0]
        ga_runs = [r for r in all_runs if r["algorithm"] == "GA" and r["dataset_size"] == ds_cap]
        
        # GA Means
        mean_alloc = statistics.mean([r["allocated_courses"] for r in ga_runs])
        mean_unalloc = statistics.mean([r["unallocated_courses"] for r in ga_runs])
        mean_c_conf = statistics.mean([r["classroom_conflicts"] for r in ga_runs])
        mean_l_conf = statistics.mean([r["lecturer_conflicts"] for r in ga_runs])
        mean_s_conf = statistics.mean([r["student_group_conflicts"] for r in ga_runs])
        mean_cap = statistics.mean([r["capacity_violations"] for r in ga_runs])
        mean_fac = statistics.mean([r["facility_violations"] for r in ga_runs])
        mean_type = statistics.mean([r["room_type_violations"] for r in ga_runs])
        mean_avail = statistics.mean([r["availability_violations"] for r in ga_runs])
        mean_util = statistics.mean([r["utilization"] for r in ga_runs])
        mean_exec = statistics.mean([r["execution_time"] for r in ga_runs])
        mean_fit = statistics.mean([r["fitness"] for r in ga_runs])
        
        # GA Stats bounds
        stats.append({
            "dataset_size": ds_cap,
            "metric": "fitness",
            "mean": mean_fit,
            "min": min([r["fitness"] for r in ga_runs]),
            "max": max([r["fitness"] for r in ga_runs]),
            "std": statistics.stdev([r["fitness"] for r in ga_runs]) if len(ga_runs) > 1 else 0
        })
        stats.append({
            "dataset_size": ds_cap,
            "metric": "execution_time",
            "mean": mean_exec,
            "min": min([r["execution_time"] for r in ga_runs]),
            "max": max([r["execution_time"] for r in ga_runs]),
            "std": statistics.stdev([r["execution_time"] for r in ga_runs]) if len(ga_runs) > 1 else 0
        })
        
        # Summary rows (comparison)
        summary.append(baseline_run)
        summary.append({
            "dataset_size": ds_cap,
            "algorithm": "GA (Mean)",
            "seed": "Multiple (5 runs)",
            "total_courses": ga_runs[0]["total_courses"],
            "allocated_courses": mean_alloc,
            "unallocated_courses": mean_unalloc,
            "classroom_conflicts": mean_c_conf,
            "lecturer_conflicts": mean_l_conf,
            "student_group_conflicts": mean_s_conf,
            "capacity_violations": mean_cap,
            "facility_violations": mean_fac,
            "room_type_violations": mean_type,
            "availability_violations": mean_avail,
            "utilization": mean_util,
            "fitness": mean_fit,
            "execution_time": mean_exec
        })
        
    with open("results/comparison/comparison_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary[0].keys())
        writer.writeheader()
        writer.writerows(summary)
        
    with open("results/comparison/statistics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["dataset_size", "metric", "mean", "min", "max", "std"])
        writer.writeheader()
        writer.writerows(stats)
        
    # Calculate Improvements
    with open("results/comparison/summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["dataset_size", "metric", "baseline_value", "ga_mean_value", "improvement_percent", "improvement_type"])
        
        for size in DATASETS:
            ds_cap = size.capitalize()
            b = [r for r in summary if r["algorithm"] == "Baseline" and r["dataset_size"] == ds_cap][0]
            g = [r for r in summary if "GA" in r["algorithm"] and r["dataset_size"] == ds_cap][0]
            
            # Conflict Reduction
            b_conflicts = b["classroom_conflicts"] + b["lecturer_conflicts"] + b["student_group_conflicts"]
            g_conflicts = g["classroom_conflicts"] + g["lecturer_conflicts"] + g["student_group_conflicts"]
            conf_imp = ((b_conflicts - g_conflicts) / b_conflicts * 100) if b_conflicts > 0 else 0
            writer.writerow([ds_cap, "Total Conflicts", b_conflicts, g_conflicts, conf_imp, "Higher is Better"])
            
            # Unallocated Reduction
            b_unalloc = b["unallocated_courses"]
            g_unalloc = g["unallocated_courses"]
            unalloc_imp = ((b_unalloc - g_unalloc) / b_unalloc * 100) if b_unalloc > 0 else 0
            writer.writerow([ds_cap, "Unallocated Courses", b_unalloc, g_unalloc, unalloc_imp, "Higher is Better"])
            
            # Utilization Improvement
            b_util = b["utilization"]
            g_util = g["utilization"]
            util_imp = ((g_util - b_util) / b_util * 100) if b_util > 0 else 0
            writer.writerow([ds_cap, "Utilization", b_util, g_util, util_imp, "Higher is Better"])
            
            # Exec Time
            b_exec = b["execution_time"]
            g_exec = g["execution_time"]
            exec_imp = ((b_exec - g_exec) / b_exec * 100) if b_exec > 0 else 0 # usually negative because GA is slower
            writer.writerow([ds_cap, "Execution Time", b_exec, g_exec, exec_imp, "Higher is Faster"])

if __name__ == "__main__":
    run_main_experiments()
