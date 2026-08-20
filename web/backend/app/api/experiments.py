from fastapi import APIRouter
import csv
import os

router = APIRouter()

@router.get("/experiments")
def get_experiments():
    base_dir = "results/experiments"
    if not os.path.exists(base_dir):
        return {}
        
    data = {}
    files = ["population_size_results.csv", "generations_results.csv", "crossover_rate_results.csv", "mutation_rate_results.csv"]
    
    for filename in files:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            key = filename.replace("_results.csv", "")
            with open(path, "r") as f:
                data[key] = list(csv.DictReader(f))
    
    return data
