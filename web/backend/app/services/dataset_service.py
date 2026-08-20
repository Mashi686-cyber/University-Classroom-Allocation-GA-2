import os
import csv
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DatasetSummary(BaseModel):
    size: str
    courses_count: int
    classrooms_count: int
    lecturers_count: int
    student_groups_count: int
    timeslots_count: int

def get_datasets() -> List[DatasetSummary]:
    summaries = []
    for size in ["small", "medium", "large"]:
        base_dir = f"data/generated/{size}"
        if not os.path.exists(base_dir):
            continue
        summaries.append(DatasetSummary(
            size=size,
            courses_count=len(load_csv(f"{base_dir}/courses.csv")),
            classrooms_count=len(load_csv(f"{base_dir}/classrooms.csv")),
            lecturers_count=len(load_csv(f"{base_dir}/lecturers.csv")),
            student_groups_count=len(load_csv(f"{base_dir}/student_groups.csv")),
            timeslots_count=len(load_csv(f"{base_dir}/timeslots.csv"))
        ))
    return summaries

def load_csv(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))
