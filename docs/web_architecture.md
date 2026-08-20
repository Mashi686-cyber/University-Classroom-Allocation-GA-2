# Web Architecture & Implementation Plan

## Goal Description
To construct a fully functional, professional web application around the existing, audited Python research implementation (UniClass-GA) without modifying or duplicating the core research algorithms. 

## User Review Required
Please review the proposed architecture, API routes, and task breakdown. The plan strictly separates the frontend (Next.js) from the backend (FastAPI), which acts as a wrapper around the existing `src/` modules.

## Proposed Changes

### 1. Backend Architecture (FastAPI)
The backend will live in `web/backend/`. It will use Python 3 and FastAPI to directly import and execute the existing research modules (`src.data`, `src.genetic_algorithm`, `src.baseline`). 
- **Job System**: To handle long-running GA optimizations, the backend will use FastAPI's `BackgroundTasks` (or `asyncio.create_task`) with a thread-safe in-memory dictionary to track job state (`queued`, `running`, `completed`, `failed`) and generation progress.
- **Result Storage**: All web-triggered runs will be safely saved in `results/web_runs/` to avoid polluting the official `results/ga/` or `results/baseline/` directories.

**Key API Endpoints:**
- `GET /api/health`
- `GET /api/datasets` (Lists small, medium, large with summary stats)
- `GET /api/datasets/{size}/{entity}` (Returns courses, classrooms, etc.)
- `POST /api/datasets/{size}/validate` (Invokes `validate_dataset(size)`)
- `GET /api/config` (Returns `GA_PARAMS`)
- `POST /api/runs` (Spawns background task for Baseline or GA)
- `GET /api/runs/{run_id}` (Returns status)
- `GET /api/runs/{run_id}/progress` (Returns current generation, fitness)
- `GET /api/runs/{run_id}/timetable` (Returns final chromosome allocation)
- `GET /api/runs/{run_id}/metrics` (Returns violations, utilization)
- `GET /api/comparison/{size}` (Parses `results/comparison/`)
- `GET /api/experiments` (Parses `results/experiments/`)
- `GET /api/analysis/{rq}` (Parses `results/analysis/`)

### 2. Frontend Architecture (Next.js)
The frontend will live in `web/frontend/` and will be initialized via `npx create-next-app@latest`.
- **Framework**: Next.js (App Router), React, TypeScript.
- **Styling**: Tailwind CSS, shadcn/ui.
- **State Management**: React Hooks (`useState`, `useEffect`) and SWR/React Query for API polling.
- **Charting**: Recharts for visualizing metrics (Conflict Comparison, Execution Time, Parameter runs).

**Key Pages:**
- `/dashboard`: High-level metrics, dataset cards, latest web run.
- `/datasets`: Data tables for Courses, Classrooms, etc., with a "Validate Dataset" button.
- `/allocation`: Form to configure GA parameters (pre-filled from `/api/config`) and a "Run Allocation" button.
- `/results`: List of all runs in `web_runs/`.
- `/results/[run_id]`: Metrics overview (Unallocated, Conflicts, Util).
- `/results/[run_id]/timetable`: Interactive grid mapping Timeslots vs Days.
- `/classrooms`: View to inspect individual classroom availability.
- `/comparison`: Recharts analyzing Baseline vs GA from official files.
- `/experiments`: Recharts for Phase 5 OFAT parameters.
- `/research`: Dashboard of Phase 6/7 findings for RQ1-RQ4.

### 3. Execution Plan
1. Create `docs/web_architecture.md` (this document serves as its foundation).
2. Initialize `web/backend` and build FastAPI routes & Job Manager.
3. Initialize `web/frontend` and install Tailwind & shadcn/ui.
4. Build Dashboard & Dataset inspection pages.
5. Build Allocation Configuration & Live Progress UI.
6. Build Timetable view & Result detail page.
7. Build Comparison & Research reporting pages using existing CSVs.
8. Perform rigorous manual browser smoke test to ensure everything connects seamlessly without mutating official research data.

## Verification Plan
### Automated Tests
- Backend tests (`pytest web/backend/tests/`) mocking the background runner.
- Existing tests (`pytest tests/`) must continue to pass without error.
### Manual Verification
- Execute full UI flow: Validate dataset -> Start GA (e.g., 10 generations for speed) -> Check progress polling -> Render timetable -> Export results.
