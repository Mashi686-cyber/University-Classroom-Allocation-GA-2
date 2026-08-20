from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import sys
import os

# Add root directory to path to allow importing src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from app.services import dataset_service
from src.data.validate_dataset import validate_dataset

router = APIRouter()

@router.get("/datasets", response_model=List[dataset_service.DatasetSummary])
def list_datasets():
    return dataset_service.get_datasets()

@router.get("/datasets/{size}/{entity}")
def get_dataset_entity(size: str, entity: str):
    if size not in ["small", "medium", "large"]:
        raise HTTPException(status_code=400, detail="Invalid dataset size")
    valid_entities = ["courses", "classrooms", "lecturers", "student_groups", "timeslots"]
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail="Invalid entity")
    
    # Due to naming convention, student_groups is student_groups.csv
    filepath = f"data/generated/{size}/{entity}.csv"
    return dataset_service.load_csv(filepath)

@router.post("/datasets/{size}/validate")
def validate_ds(size: str):
    if size not in ["small", "medium", "large"]:
        raise HTTPException(status_code=400, detail="Invalid dataset size")
    
    errors, warnings = validate_dataset(size)
    status = "PASS"
    if errors > 0:
        status = "ERROR"
    elif warnings > 0:
        status = "WARNING"
        
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "message": f"Validation complete: {errors} Errors, {warnings} Warnings."
    }
