# UniClass-GA Final Submission Package Manifest

**Package Name:** UniClass-GA-Final-Submission.zip
**Package Size:** 980376 bytes
**File Count:** 214

## Included Directories
- `src/` (Genetic Algorithm, Baseline, Constraints, Models)
- `data/` (Research Datasets)
- `results/` (Research Figures, Analysis, Official Output Data)
- `web/` (FastAPI Backend, Next.js Frontend)
- `docs/` (Final Report, Timetable Run-time Fixes, Matrices)
- `tests/` (Automated Engine Tests)

## Excluded Directories / Files
- `.venv/` (Python virtual environments)
- `node_modules/` (Node.js dependencies)
- `.next/` (Next.js build cache)
- `__pycache__/` and `.pytest_cache/` (Python caches)
- `.git/`
- `*.log` (Debug logs)
- Scratch scripts (e.g., `test_browser.js`, `debug.html`)
- Temporary UI results in `results/web_runs/`

## Verification Status

### Tests Result
- **Python Engine Tests**: 29/29 Passed (pytest `tests/`)
- **Backend API Tests**: 4/4 Passed (pytest `web/backend/tests/`)
- **Total Tests**: 33 Passed

### Frontend Build Result
- **Status**: SUCCESS (`npm run build`)
- **Environment**: Next.js 16.3.1 (Turbopack)
- **Zero TypeErrors**

### Launcher Verification
- **Status**: SUCCESS
- Tested `start.py --check` against the fresh extracted sandbox.
- Correctly parsed the `UniClass-GA-FINAL` execution root.
- Verified dependencies and datasets are reachable.

### Timetable Browser Verification
- **Status**: SUCCESS
- **Mechanism**: Headless Chromium (Puppeteer DOM parsing)
- **Baseline Algorithm**: Rendered course blocks properly across the UI grid.
- **Genetic Algorithm**: Processed the flattened best_chromosome list and rendered successfully.
- **Multi-Slot Routing**: Verified that multi-slot strings (e.g., `TS001,TS002`) accurately generate duplicate DOM blocks over multiple HTML table cells.
- **Error Handling**: Gracefully managed HTTP 404 Runs (`Run Not Found`) and Backend Server Downtime (`API Unreachable`) without raising React Hydration faults.
