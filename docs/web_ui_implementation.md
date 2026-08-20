# Web UI Implementation Report

This document summarizes the architectural and implementation details of the Web Application built around the UniClass GA research system.

## 1. Architecture Overview

The web application follows a strict separation of concerns, utilizing a headless backend API that wraps the original research codebase, paired with a React-based frontend.

*   **Frontend:** Next.js 14 (App Router), React, TypeScript, Tailwind CSS, shadcn/ui.
*   **Backend:** FastAPI, Python 3, Pydantic.
*   **Core Logic:** The original `src/` modules (`genetic_algorithm`, `baseline`, `evaluation`) remain unchanged and act as the core processing engine.

## 2. Frontend Implementation

The frontend is located in `web/frontend/` and provides a modern, responsive, university-styled dashboard.
*   **Routing:** Utilizes Next.js App Router (`/dashboard`, `/datasets`, `/allocation`, `/results/[runId]`, `/classrooms`, `/comparison`, `/experiments`, `/research`).
*   **UI Components:** Customized `shadcn/ui` components (Cards, Badges, Tabs, Tables) ensure a professional aesthetic.
*   **Data Visualization:** Uses `recharts` to render interactive analytical charts comparing the Baseline against the GA, and displaying OFAT parameter experiment results.
*   **State Management:** React hooks manage API polling for live job statuses.

## 3. Backend API Implementation

The backend is located in `web/backend/` and exposes REST endpoints.
*   **Job System:** To prevent blocking the main HTTP thread during long-running GA optimizations, the `POST /api/runs` endpoint uses FastAPI's `BackgroundTasks` to execute the algorithm asynchronously. Job state is tracked in memory and saved to `results/web_runs/`.
*   **Endpoints:**
    *   `GET /api/datasets`: Lists dataset summaries.
    *   `POST /api/datasets/{size}/validate`: Invokes `src.data.validate_dataset.validate_dataset`.
    *   `GET /api/config`: Retrieves official `GA_PARAMS`.
    *   `POST /api/runs`: Submits optimization tasks.
    *   `GET /api/runs/{run_id}`: Retrieves job status and constraint metrics.
    *   `GET /api/comparison/{size}`: Serves parsed CSV data from official research results.

## 4. Integration with Existing Python Modules

A critical rule of this implementation was the strict preservation of the existing Python research algorithms.
*   **No Duplication:** No GA logic (crossover, mutation, fitness) was recreated in JavaScript/TypeScript.
*   **Execution:** The backend imports `GeneticAlgorithm` and `BaselineAllocator` directly from the `src/` directory, formats the resulting `Chromosome` or allocation dictionaries into JSON, and serves them to the frontend.
*   **Validation:** The web UI validation button directly invokes the CLI-designed `validate_dataset.py` logic, adapting its stdout logic into structured API responses.

## 5. Result Handling and Reproducibility

To ensure the integrity of the original research findings:
*   User-triggered web runs are saved exclusively to `results/web_runs/`.
*   The web application reads official analytical CSVs from `results/comparison/` and `results/experiments/` to render charts but never modifies them.

## 6. Testing & Browser Verification

*   **Backend:** Pytest tests verify that the FastAPI endpoints load successfully and respond with the correct JSON schema.
*   **Frontend Check:** The Next.js build (`npm run build`) completed successfully with 0 TypeScript/ESLint errors.
*   **Browser Smoke Test:** We verified via curl that both the frontend Next.js server (Port 3000) and the backend FastAPI server (Port 8000) are running and responding correctly, forming a fully integrated pipeline.

## 7. How to Run

**Start Backend:**
```bash
cd web/backend
../../.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend:**
```bash
cd web/frontend
npm run dev
```

The application will be accessible at `http://localhost:3000`.
