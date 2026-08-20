# University-Classroom-Allocation-GA
University Classroom Allocation Optimization Using Genetic Algorithm for IT41033 Nature Inspired Algorithm Mini Project.

## Dataset Generation

Because finding a real-world, highly constrained university classroom allocation dataset is difficult, we use a robust synthetic data generator that creates realistic dependencies (courses to lecturers, student groups to classroom capacities, facility requirements, etc.).

### How to Regenerate the Dataset
To generate the Small, Medium, and Large datasets from scratch, run the generator script from the project root:

```bash
python3 src/data/generate_synthetic_data.py
```

This will create or overwrite the CSV files in `data/generated/small/`, `data/generated/medium/`, and `data/generated/large/`.

### Validation
To ensure referential integrity and data validity across all generated datasets, run the validation script:

```bash
python3 src/data/validate_dataset.py
```

## Baseline Allocation

To run the simple greedy baseline allocator on all datasets and generate evaluation metrics:

```bash
export PYTHONPATH=.
python3 src/baseline/baseline_allocator.py
```

Results and summaries will be saved in `results/baseline/`.

## Results Analysis and Visualization

To programmatically analyze the experimental results and generate the descriptive statistics and research metric tables (RQ1-RQ4):

```bash
export PYTHONPATH=.
python3 src/analysis/analyze_results.py
```
This will generate CSV tables in `results/analysis/`.

To generate the publication-quality visualization figures (using `matplotlib`):

```bash
export PYTHONPATH=.
python3 src/analysis/create_figures.py
```
This will output PNG files to `results/figures/`.

## Web Application UI

UniClass-GA now includes a full functional web user interface built with Next.js and FastAPI that acts as a wrapper around the existing Python research algorithms.

### Easiest method (One-Command Launcher)

You can launch the entire Web UI stack (Backend + Frontend) with a single cross-platform command. The launcher will automatically detect your environment, install dependencies if necessary, and open your browser.

**Linux / macOS:**
```bash
./start.sh
```

**Windows Command Prompt:**
```bash
start.bat
```

**Windows PowerShell:**
```bash
.\start.ps1
```

**Universal / Cross-platform:**
```bash
python start.py
```

*For first-time setup on a fresh machine, run:*
```bash
python start.py --setup
```

For more details on the launcher capabilities (like disabling auto-browser opening or changing ports), see `docs/launcher.md`. For UI operating instructions, see `docs/web_ui_user_guide.md`.


### Starting the Backend (FastAPI)
```bash
cd web/backend
../../.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Starting the Frontend (Next.js)
```bash
cd web/frontend
npm run dev
```

The Web UI will be available at `http://localhost:3000`. For more details, see `docs/web_ui_user_guide.md`.
