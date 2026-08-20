from fastapi import APIRouter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
from src.genetic_algorithm.config import GA_PARAMS

router = APIRouter()

@router.get("/config")
def get_config():
    return GA_PARAMS
