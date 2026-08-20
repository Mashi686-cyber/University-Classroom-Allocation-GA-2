import csv
import statistics
import os

def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return list(csv.DictReader(f))

def write_csv(path, headers, rows):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def analyze_descriptive_statistics(all_runs):
    headers = [
        "Dataset", "Metric", "Mean", "Median", "Min", "Max", "StdDev"
    ]
    rows = []
    
    datasets = ["Small", "Medium", "Large"]
    metrics = [
        "fitness", "allocated_courses", "unallocated_courses", 
        "classroom_conflicts", "lecturer_conflicts", "student_group_conflicts",
        "capacity_violations", "facility_violations", "room_type_violations", 
        "availability_violations", "utilization", "execution_time"
    ]
    
    for ds in datasets:
        ga_runs = [r for r in all_runs if r["algorithm"] == "GA" and r["dataset_size"] == ds]
        if not ga_runs: continue
        
        for metric in metrics:
            # Calculate total conflicts specially
            if metric == "total_conflicts":
                values = [float(r["classroom_conflicts"]) + float(r["lecturer_conflicts"]) + float(r["student_group_conflicts"]) for r in ga_runs]
            else:
                values = [float(r[metric]) for r in ga_runs]
            
            mean_val = statistics.mean(values)
            median_val = statistics.median(values)
            min_val = min(values)
            max_val = max(values)
            std_val = statistics.stdev(values) if len(values) > 1 else 0.0
            
            rows.append([ds, metric, f"{mean_val:.2f}", f"{median_val:.2f}", f"{min_val:.2f}", f"{max_val:.2f}", f"{std_val:.2f}"])
            
        # Manually do total_conflicts
        values = [float(r["classroom_conflicts"]) + float(r["lecturer_conflicts"]) + float(r["student_group_conflicts"]) for r in ga_runs]
        mean_val = statistics.mean(values)
        median_val = statistics.median(values)
        min_val = min(values)
        max_val = max(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0.0
        rows.append([ds, "total_conflicts", f"{mean_val:.2f}", f"{median_val:.2f}", f"{min_val:.2f}", f"{max_val:.2f}", f"{std_val:.2f}"])

    write_csv("results/analysis/descriptive_statistics.csv", headers, rows)

def analyze_rq1_conflict_reduction(all_runs):
    headers = [
        "Dataset", "Baseline conflicts", "GA mean conflicts", "GA minimum conflicts", 
        "GA maximum conflicts", "Conflict reduction %",
        "Classroom Conflicts (Base->GA)", "Lecturer Conflicts (Base->GA)", "Student Group Conflicts (Base->GA)"
    ]
    rows = []
    datasets = ["Small", "Medium", "Large"]
    for ds in datasets:
        base_runs = [r for r in all_runs if r["algorithm"] == "Baseline" and r["dataset_size"] == ds]
        ga_runs = [r for r in all_runs if r["algorithm"] == "GA" and r["dataset_size"] == ds]
        if not base_runs or not ga_runs: continue
        
        b = base_runs[0]
        b_c = float(b["classroom_conflicts"]) + float(b["lecturer_conflicts"]) + float(b["student_group_conflicts"])
        
        g_c_list = [float(r["classroom_conflicts"]) + float(r["lecturer_conflicts"]) + float(r["student_group_conflicts"]) for r in ga_runs]
        g_mean = statistics.mean(g_c_list)
        g_min = min(g_c_list)
        g_max = max(g_c_list)
        
        red_pct = ((b_c - g_mean) / b_c * 100) if b_c > 0 else 0.0
        
        g_class_mean = statistics.mean([float(r["classroom_conflicts"]) for r in ga_runs])
        g_lect_mean = statistics.mean([float(r["lecturer_conflicts"]) for r in ga_runs])
        g_stud_mean = statistics.mean([float(r["student_group_conflicts"]) for r in ga_runs])
        
        rows.append([
            ds, b_c, f"{g_mean:.2f}", f"{g_min:.2f}", f"{g_max:.2f}", f"{red_pct:.2f}%",
            f"{b['classroom_conflicts']} -> {g_class_mean:.2f}",
            f"{b['lecturer_conflicts']} -> {g_lect_mean:.2f}",
            f"{b['student_group_conflicts']} -> {g_stud_mean:.2f}"
        ])
    write_csv("results/analysis/rq1_conflict_analysis.csv", headers, rows)

def analyze_rq2_utilization(all_runs):
    headers = [
        "Dataset", "Allocated Courses", "Baseline utilization", "GA mean utilization",
        "GA standard deviation", "Absolute change in percentage points", "Relative percentage change"
    ]
    rows = []
    datasets = ["Small", "Medium", "Large"]
    for ds in datasets:
        base_runs = [r for r in all_runs if r["algorithm"] == "Baseline" and r["dataset_size"] == ds]
        ga_runs = [r for r in all_runs if r["algorithm"] == "GA" and r["dataset_size"] == ds]
        if not base_runs or not ga_runs: continue
        
        b = base_runs[0]
        b_u = float(b["utilization"])
        
        g_u_list = [float(r["utilization"]) for r in ga_runs]
        g_mean = statistics.mean(g_u_list)
        g_std = statistics.stdev(g_u_list) if len(g_u_list) > 1 else 0.0
        
        abs_change = g_mean - b_u
        rel_change = (abs_change / b_u * 100) if b_u > 0 else 0.0
        
        rows.append([
            ds, b["allocated_courses"], f"{b_u:.2f}%", f"{g_mean:.2f}%", f"{g_std:.2f}",
            f"{abs_change:.2f} pp", f"{rel_change:.2f}%"
        ])
    write_csv("results/analysis/rq2_utilization_analysis.csv", headers, rows)

def analyze_rq3_parameters():
    headers = [
        "Parameter Type", "Parameter Value", "Final fitness", "Utilization", "Execution time", "Best generation"
    ]
    rows = []
    
    files = {
        "Population Size": "results/experiments/population_size_results.csv",
        "Generations": "results/experiments/generations_results.csv",
        "Mutation Rate": "results/experiments/mutation_rate_results.csv",
        "Crossover Rate": "results/experiments/crossover_rate_results.csv"
    }
    
    for p_type, path in files.items():
        data = load_csv(path)
        for r in data:
            rows.append([
                p_type, r["value"], f"{float(r['final_fitness']):.2f}", 
                f"{float(r['utilization']):.2f}%", f"{float(r['execution_time']):.2f}", r["best_generation"]
            ])
            
    write_csv("results/analysis/rq3_parameter_analysis.csv", headers, rows)

def analyze_rq4_comparison(summary_data):
    headers = [
        "Dataset", "Algorithm", "Allocated", "Unallocated", "Total conflicts",
        "Capacity violations", "Facility violations", "Room type violations",
        "Utilization", "Execution time"
    ]
    rows = []
    
    for r in summary_data:
        alg = r["algorithm"]
        # Format numbers cleanly
        tot_c = float(r["classroom_conflicts"]) + float(r["lecturer_conflicts"]) + float(r["student_group_conflicts"])
        rows.append([
            r["dataset_size"], alg, r["allocated_courses"], r["unallocated_courses"],
            f"{tot_c:.1f}", f"{float(r['capacity_violations']):.1f}", 
            f"{float(r['facility_violations']):.1f}", f"{float(r['room_type_violations']):.1f}",
            f"{float(r['utilization']):.1f}%", f"{float(r['execution_time']):.2f}s"
        ])
        
    write_csv("results/analysis/rq4_comparison_analysis.csv", headers, rows)

if __name__ == "__main__":
    all_runs = load_csv("results/comparison/all_runs.csv")
    summary = load_csv("results/comparison/comparison_results.csv")
    
    analyze_descriptive_statistics(all_runs)
    analyze_rq1_conflict_reduction(all_runs)
    analyze_rq2_utilization(all_runs)
    analyze_rq3_parameters()
    analyze_rq4_comparison(summary)
    print("Analysis tables generated successfully.")
