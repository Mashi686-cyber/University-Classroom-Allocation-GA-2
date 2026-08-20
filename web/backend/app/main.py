import os
import sys
# Change working directory to project root so relative paths work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
os.chdir(project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web.backend.app.api import datasets, runs, config, experiments, analysis

app = FastAPI(title="UniClass GA API", description="API for University Classroom Allocation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router, prefix="/api")
app.include_router(runs.router, prefix="/api")
app.include_router(config.router, prefix="/api")
app.include_router(experiments.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
