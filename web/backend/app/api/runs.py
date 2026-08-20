from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services import job_service
import os
import json

router = APIRouter()

class RunRequest(BaseModel):
    dataset_size: str
    algorithm: str
    population_size: Optional[int] = 50
    generations: Optional[int] = 50
    crossover_rate: Optional[float] = 0.8
    mutation_rate: Optional[float] = 0.1
    elitism: Optional[int] = 2
    random_seed: Optional[int] = 42

@router.post("/runs")
def create_run(req: RunRequest, background_tasks: BackgroundTasks):
    if req.dataset_size not in ["small", "medium", "large"]:
        raise HTTPException(status_code=400, detail="Invalid dataset size")
    if req.algorithm not in ["baseline", "ga"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm")
        
    if req.algorithm == "ga":
        if req.population_size is None or req.population_size <= 0:
            raise HTTPException(status_code=400, detail="Population size must be > 0")
        if req.generations is None or req.generations <= 0:
            raise HTTPException(status_code=400, detail="Generations must be > 0")
        if req.crossover_rate is None or not (0 <= req.crossover_rate <= 1):
            raise HTTPException(status_code=400, detail="Crossover rate must be between 0 and 1")
        if req.mutation_rate is None or not (0 <= req.mutation_rate <= 1):
            raise HTTPException(status_code=400, detail="Mutation rate must be between 0 and 1")
        
    params = {
        "population_size": req.population_size,
        "generations": req.generations,
        "crossover_rate": req.crossover_rate,
        "mutation_rate": req.mutation_rate,
        "elitism": req.elitism,
        "random_seed": req.random_seed
    }
    
    run_id = job_service.submit_job(req.dataset_size, req.algorithm, params)
    background_tasks.add_task(job_service.run_job, run_id)
    
    return {"run_id": run_id, "status": "queued"}

@router.get("/runs")
def list_runs():
    # Load from web_runs directory as well
    os.makedirs("results/web_runs", exist_ok=True)
    all_runs = []
    
    # Add active memory jobs
    memory_ids = set()
    for job in job_service.get_all_jobs():
        memory_ids.add(job["run_id"])
        all_runs.append({
            "run_id": job["run_id"],
            "dataset_size": job["dataset_size"],
            "algorithm": job["algorithm"],
            "status": job["status"],
            "timestamp": job["timestamp"]
        })
        
    # Add saved jobs not in memory
    for file in os.listdir("results/web_runs"):
        if file.endswith(".json"):
            run_id = file.replace(".json", "")
            if run_id not in memory_ids:
                with open(f"results/web_runs/{file}", "r") as f:
                    try:
                        data = json.load(f)
                        all_runs.append({
                            "run_id": data["run_id"],
                            "dataset_size": data["dataset_size"],
                            "algorithm": data["algorithm"],
                            "status": data["status"],
                            "timestamp": data["timestamp"]
                        })
                    except:
                        pass
                        
    # Sort by timestamp desc
    all_runs.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return all_runs

@router.get("/runs/{run_id}")
def get_run_status(run_id: str):
    job = job_service.get_job(run_id)
    if not job:
        path = f"results/web_runs/{run_id}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        raise HTTPException(status_code=404, detail="Run not found")
    return job

@router.get("/runs/{run_id}/progress")
def get_run_progress(run_id: str):
    job = job_service.get_job(run_id)
    if not job:
        raise HTTPException(status_code=404, detail="Run not found in active memory")
    return {"status": job["status"]}

@router.get("/runs/{run_id}/metrics")
def get_run_metrics(run_id: str):
    data = get_run_status(run_id)
    if data["status"] != "completed":
        raise HTTPException(status_code=400, detail="Run not completed")
    return data["result"]

@router.get("/runs/{run_id}/timetable")
def get_run_timetable(run_id: str):
    data = get_run_status(run_id)
    if data["status"] != "completed":
        raise HTTPException(status_code=400, detail="Run not completed")
    
    if data["algorithm"] == "baseline":
        return data["result"].get("best_chromosome", [])
    elif data["algorithm"] == "ga":
        return data["result"].get("best_chromosome", [])
    
    return []
