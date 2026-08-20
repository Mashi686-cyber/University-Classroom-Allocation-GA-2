import os
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return list(csv.DictReader(f))

def save_fig(name):
    plt.tight_layout()
    plt.savefig(f"results/figures/{name}", dpi=300)
    plt.close()

def plot_comparison(summary_data):
    datasets = ["Small", "Medium", "Large"]
    base_conflicts, ga_conflicts = [], []
    base_util, ga_util = [], []
    base_alloc, ga_alloc = [], []
    base_exec, ga_exec = [], []
    
    for ds in datasets:
        b = [r for r in summary_data if r["algorithm"] == "Baseline" and r["dataset_size"] == ds][0]
        g = [r for r in summary_data if "GA" in r["algorithm"] and r["dataset_size"] == ds][0]
        
        b_c = float(b["classroom_conflicts"]) + float(b["lecturer_conflicts"]) + float(b["student_group_conflicts"])
        g_c = float(g["classroom_conflicts"]) + float(g["lecturer_conflicts"]) + float(g["student_group_conflicts"])
        base_conflicts.append(b_c)
        ga_conflicts.append(g_c)
        
        base_util.append(float(b["utilization"]))
        ga_util.append(float(g["utilization"]))
        
        base_alloc.append(int(b["allocated_courses"]))
        ga_alloc.append(float(g["allocated_courses"])) # mean
        
        base_exec.append(float(b["execution_time"]))
        ga_exec.append(float(g["execution_time"]))
        
    x = np.arange(len(datasets))
    width = 0.35
    
    # FIG 1: Conflicts
    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, base_conflicts, width, label='Baseline')
    plt.bar(x + width/2, ga_conflicts, width, label='GA (Mean)')
    plt.xlabel('Dataset Size')
    plt.ylabel('Total Conflicts')
    plt.title('Baseline vs GA — Total Conflicts')
    plt.xticks(x, datasets)
    plt.legend()
    save_fig('fig01_conflict_comparison.png')

    # FIG 2: Utilization
    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, base_util, width, label='Baseline')
    plt.bar(x + width/2, ga_util, width, label='GA (Mean)')
    plt.xlabel('Dataset Size')
    plt.ylabel('Utilization (%)')
    plt.title('Baseline vs GA — Classroom Utilization')
    plt.xticks(x, datasets)
    plt.legend()
    save_fig('fig02_utilization_comparison.png')
    
    # FIG 3: Allocated Courses
    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, base_alloc, width, label='Baseline')
    plt.bar(x + width/2, ga_alloc, width, label='GA (Mean)')
    plt.xlabel('Dataset Size')
    plt.ylabel('Allocated Courses')
    plt.title('Baseline vs GA — Allocated Courses')
    plt.xticks(x, datasets)
    plt.legend()
    save_fig('fig03_allocated_courses.png')
    
    # FIG 4: Execution Time
    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, base_exec, width, label='Baseline')
    plt.bar(x + width/2, ga_exec, width, label='GA (Mean)')
    plt.xlabel('Dataset Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Baseline vs GA — Execution Time')
    plt.xticks(x, datasets)
    plt.legend()
    save_fig('fig04_execution_time.png')

def plot_parameters():
    # FIG 5 & 6: Population Size
    data = load_csv("results/experiments/population_size_results.csv")
    x = [int(r["value"]) for r in data]
    f = [float(r["final_fitness"]) for r in data]
    e = [float(r["execution_time"]) for r in data]
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, f, marker='o')
    plt.xlabel('Population Size')
    plt.ylabel('Final Fitness')
    plt.title('Population Size vs Final Fitness')
    plt.grid(True)
    save_fig('fig05_population_fitness.png')
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, e, marker='o', color='orange')
    plt.xlabel('Population Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Population Size vs Execution Time')
    plt.grid(True)
    save_fig('fig06_population_time.png')
    
    # FIG 7 & 8: Generations
    data = load_csv("results/experiments/generations_results.csv")
    x = [int(r["value"]) for r in data]
    f = [float(r["final_fitness"]) for r in data]
    e = [float(r["execution_time"]) for r in data]
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, f, marker='o')
    plt.xlabel('Generations')
    plt.ylabel('Final Fitness')
    plt.title('Generations vs Final Fitness')
    plt.grid(True)
    save_fig('fig07_generations_fitness.png')
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, e, marker='o', color='orange')
    plt.xlabel('Generations')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Generations vs Execution Time')
    plt.grid(True)
    save_fig('fig08_generations_time.png')
    
    # FIG 9: Mutation
    data = load_csv("results/experiments/mutation_rate_results.csv")
    x = [float(r["value"]) for r in data]
    f = [float(r["final_fitness"]) for r in data]
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, f, marker='o')
    plt.xlabel('Mutation Rate')
    plt.ylabel('Final Fitness')
    plt.title('Mutation Rate vs Final Fitness')
    plt.grid(True)
    save_fig('fig09_mutation_fitness.png')
    
    # FIG 10: Crossover
    data = load_csv("results/experiments/crossover_rate_results.csv")
    x = [float(r["value"]) for r in data]
    f = [float(r["final_fitness"]) for r in data]
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, f, marker='o')
    plt.xlabel('Crossover Rate')
    plt.ylabel('Final Fitness')
    plt.title('Crossover Rate vs Final Fitness')
    plt.grid(True)
    save_fig('fig10_crossover_fitness.png')

def plot_large_seeds(all_runs):
    # FIG 12
    large_runs = [r for r in all_runs if r["dataset_size"] == "Large" and r["algorithm"] == "GA"]
    seeds = [r["seed"] for r in large_runs]
    conf = [float(r["classroom_conflicts"]) + float(r["lecturer_conflicts"]) + float(r["student_group_conflicts"]) for r in large_runs]
    
    plt.figure(figsize=(8, 5))
    plt.bar(seeds, conf, color='red')
    plt.xlabel('Seed')
    plt.ylabel('Total Conflicts')
    plt.title('Large Dataset — Five Seed Results (Conflicts)')
    
    # Annotate fitness & util
    for i, r in enumerate(large_runs):
        plt.text(i, conf[i] + 0.05, f"Fit: {float(r['fitness']):.0f}\nUtil: {float(r['utilization']):.1f}%", ha='center', fontsize=9)
        
    save_fig('fig12_large_seed_analysis.png')

if __name__ == "__main__":
    summary = load_csv("results/comparison/comparison_results.csv")
    all_runs = load_csv("results/comparison/all_runs.csv")
    
    plot_comparison(summary)
    plot_parameters()
    plot_large_seeds(all_runs)
    print("Figures generated successfully (Figure 11 omitted due to missing history data).")
