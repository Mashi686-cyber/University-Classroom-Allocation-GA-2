# Submission Manifest

This document outlines the exact files and directories that must be included in the final academic submission package, as well as the artifacts that must be excluded.

## Included Files (To Be Submitted)

**A. Final Report**
- `docs/final_report.md` (The complete academic research report)

**B. Source Code**
- `src/baseline/baseline_allocator.py`
- `src/data/generate_synthetic_data.py`
- `src/data/validate_dataset.py`
- `src/evaluation/constraint_checker.py`
- `src/evaluation/metrics.py`
- `src/experiments/main_experiments.py`
- `src/experiments/parameter_experiments.py`
- `src/genetic_algorithm/chromosome.py`
- `src/genetic_algorithm/config.py`
- `src/genetic_algorithm/crossover.py`
- `src/genetic_algorithm/fitness.py`
- `src/genetic_algorithm/genetic_algorithm.py`
- `src/genetic_algorithm/mutation.py`
- `src/genetic_algorithm/selection.py`
- `src/analysis/analyze_results.py`
- `src/analysis/create_figures.py`
- *(And all `__init__.py` files in `src/`)*

**C. Dataset**
- `data/generated/small/*.csv`
- `data/generated/medium/*.csv`
- `data/generated/large/*.csv`

**D. Experimental Results**
- `results/comparison/*.csv`
- `results/experiments/*.csv`
- `results/analysis/*.csv`

**E. Figures**
- `results/figures/*.png`

**F. Documentation**
- `docs/baseline_method.md`
- `docs/citation_audit.md`
- `docs/dataset_design.md`
- `docs/evaluation_definitions.md`
- `docs/final_project_audit.md`
- `docs/final_report_quality_check.md`
- `docs/final_results_check.md`
- `docs/final_submission_check.md`
- `docs/ga_design.md`
- `docs/parameter_experiments.md`
- `docs/phase6_audit.md`
- `docs/phase7_methodology.md`
- `docs/project_structure_audit.md`
- `docs/proposal_vs_final_audit.md`
- `docs/results_discussion.md`
- `docs/rq_analysis.md`
- `docs/rq_evidence_matrix.md`

**G. Tests**
- `tests/test_baseline.py`
- `tests/test_experiments.py`
- `tests/test_fitness.py`
- `tests/test_genetic_algorithm.py`

**H. Requirements/Dependencies**
- (Include `requirements.txt` if generated, otherwise note `matplotlib` dependency)

**I. README**
- `README.md`

---

## Excluded Files (Do NOT Submit)

The following files are intermediate, temporary, or cache artifacts and must **not** be included in the final zip package:
- `.venv/` (Virtual environment)
- `__pycache__/` and `.pytest_cache/`
- `.gemini/` or any IDE-specific folders
- Raw downloaded kaggle archives in root (`archive.zip`, `assessments.csv`, etc.)
- Temporary root scripts (`analyze.py`, `analyze_feasibility.py`, `audit_*.py`, `parse_results.py`, `test_reproducibility.py`)
- Temporary `.json` dumps in the root folder.
