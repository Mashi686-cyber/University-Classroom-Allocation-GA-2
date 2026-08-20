import uuid
import os
import time
import json
import csv
from typing import Dict, Any

from src.experiments.main_experiments import load_dataset
from src.baseline.baseline_allocator import BaselineAllocator
from src.evaluation.constraint_checker import ConstraintChecker
from src.evaluation.metrics import MetricsCalculator
from src.genetic_algorithm.genetic_algorithm import GeneticAlgorithm

# In-memory job store
jobs = {}

def submit_job(dataset_size: str, algorithm: str, params: dict):
    run_id = str(uuid.uuid4())
    jobs[run_id] = {
        "run_id": run_id,
        "dataset_size": dataset_size,
        "algorithm": algorithm,
        "params": params,
        "status": "queued",
        "progress": {},
        "result": None,
        "error": None,
        "timestamp": time.time()
    }
    return run_id

def get_job(run_id: str):
    return jobs.get(run_id)

def get_all_jobs():
    return list(jobs.values())

def run_job(run_id: str):
    job = jobs[run_id]
    job["status"] = "running"
    try:
        courses, classrooms, timeslots = load_dataset(job["dataset_size"])
        
        if job["algorithm"] == "baseline":
            start_time = time.time()
            allocator = BaselineAllocator(courses, classrooms, timeslots)
            allocations = allocator.allocate()
            exec_time = time.time() - start_time
            
            checker = ConstraintChecker(courses, classrooms, timeslots)
            violations = checker.evaluate(allocations)
            
            metrics_calc = MetricsCalculator(classrooms)
            util, _ = metrics_calc.calculate_utilization(allocations)
            
            job["result"] = {
                "algorithm": "Baseline",
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
                "fitness": None,
                "execution_time": exec_time,
                "best_chromosome": allocations
            }
        elif job["algorithm"] == "ga":
            config = job.get("params", {})
            ga = GeneticAlgorithm(courses, classrooms, timeslots, config=config)
            res = ga.run()
            
            alloc_count = len([g for g in res["best_chromosome"].genes.values() if g[0] is not None])
            job["result"] = {
                "algorithm": "GA",
                "total_courses": len(courses),
                "allocated_courses": alloc_count,
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
                "execution_time": res["execution_time_seconds"],
                "best_chromosome": res["best_chromosome"].to_allocations(courses)
            }
        
        job["status"] = "completed"
        save_web_run(job)
        
    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)

def save_web_run(job):
    os.makedirs("results/web_runs", exist_ok=True)
    with open(f"results/web_runs/{job['run_id']}.json", "w") as f:
        json.dump(job, f, indent=4)
