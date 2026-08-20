# Run Detail Page Runtime Fix

## 1. Original Error
The `/results/[runId]` (Run Detail) page was throwing a React runtime error:
`Runtime TypeError: Cannot read properties of undefined (reading 'allocated_courses')`

This occurred specifically on the `MetricBlock` component when rendering:
```javascript
<MetricBlock label="Allocated" value={`${job.result.allocated_courses} / ${job.result.total_courses}`} />
```

## 2. Actual API Response
When inspecting the API response from `GET /api/runs/{runId}` for completed jobs, the structure is as follows:

```json
{
  "run_id": "406bca29-9d80-4801-aa2a-a77e32a682c3",
  "dataset_size": "small",
  "algorithm": "ga",
  "status": "completed",
  "result": {
    "algorithm": "GA",
    "total_courses": 20,
    "allocated_courses": 17,
    "unallocated_courses": 3,
    "classroom_conflicts": 0,
    "lecturer_conflicts": 0,
    "student_group_conflicts": 0,
    "utilization": 70.99,
    "fitness": -299929.0,
    "execution_time": 0.36
  },
  "error": null
}
```

For jobs that are still `running`, `queued`, or `failed`, the `result` property might be missing or `null`.

## 3. Root Cause
The root cause of the bug was that the frontend page was attempting to immediately access `job.result.allocated_courses` assuming that if a job had a `status === 'completed'`, `job.result` would unconditionally exist. It also fell through to the metrics display even if a job state was unknown or if the `result` was mysteriously `null`. Moreover, typing `job` as `any` hid this problem from the TypeScript compiler.

## 4. Backend/API Contract
The backend API successfully returns all normalized keys within the `result` object (both GA and Baseline runs return `allocated_courses`, `unallocated_courses`, `total_courses`, `utilization`, etc.). `fitness` is explicitly `null` for the baseline algorithm.

## 5. Frontend Type Fix
In `web/frontend/src/app/results/[runId]/page.tsx`, we eliminated the `any` fallback and implemented a strict `RunJob` and `RunResult` TypeScript definition:

```typescript
type RunResult = {
  algorithm: string;
  total_courses: number;
  allocated_courses: number;
  unallocated_courses: number;
  classroom_conflicts: number;
  lecturer_conflicts: number;
  student_group_conflicts: number;
  capacity_violations: number;
  facility_violations: number;
  room_type_violations: number;
  availability_violations: number;
  utilization: number;
  fitness: number | null;
  execution_time: number;
  best_chromosome: any[];
};

type RunJob = {
  run_id: string;
  dataset_size: string;
  algorithm: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress: any;
  result?: RunResult | null;
  error?: string | null;
  timestamp: number;
};
```

## 6. Job-State Handling
The React component was restructured to handle missing `result` gracefully without crashing:
- Handled `queued` / `running` states.
- Handled `failed` state cleanly showing `job.error`.
- For `completed` runs missing a result block, we now render a safe fallback UI: `Result Data Unavailable`.
- Safe rendering of `utilization` percentage and `fitness` only when available.

## 7. Baseline Verification
Verified against a completed Baseline run (`runId: 8e10363a-c9e4-4ab8-a3a2-55a2fc9fc122`).
Metrics including `17 / 20` (allocated vs total) and execution time render accurately. `fitness` is cleanly omitted.

## 8. GA Verification
Verified against a completed Genetic Algorithm run (`runId: 406bca29-9d80-4801-aa2a-a77e32a682c3`).
Metrics including negative fitness values and `71.0%` utilization format and render correctly without console errors.

## 9. Browser Verification
An end-to-end headless Puppeteer verification test (`test_run.js`) was executed against both routes confirming that the run detail metrics load correctly in the DOM (e.g. `17 / 20`) without any `TypeError` crashes or hydration errors.

## 10. Build Result
The Next.js frontend rebuilds cleanly:
```bash
> frontend@0.1.0 build
> next build
✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages (13/13)
```

## 11. Test Result
Python backend and core algorithm tests pass 100%.
```bash
========================= 29 passed in 1.06s =========================
========================= 4 passed, 1 warning in 0.22s =========================
```
