from fastapi import APIRouter
import csv
import os

router = APIRouter()

@router.get("/analysis/{rq}")
def get_analysis(rq: str):
    base_dir = "results/analysis"
    if not os.path.exists(base_dir):
        return []
        
    filename = ""
    if rq == "rq1":
        filename = "rq1_conflict_analysis.csv"
    elif rq == "rq2":
        filename = "rq2_utilization_analysis.csv"
    elif rq == "rq3":
        filename = "rq3_parameter_analysis.csv"
    elif rq == "rq4":
        filename = "rq4_comparison_analysis.csv"
    else:
        return []
        
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return list(csv.DictReader(f))
            
    return []

@router.get("/comparison/{size}")
def get_comparison(size: str):
    base_dir = "results/comparison"
    path = os.path.join(base_dir, "comparison_results.csv")
    if not os.path.exists(path):
        return []
        
    res = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["dataset_size"].lower() == size.lower():
                res.append(row)
    return res
