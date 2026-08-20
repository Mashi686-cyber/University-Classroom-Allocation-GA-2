# Phase 7 Methodology

## Analysis Methodology
The experimental analysis was conducted strictly utilizing the pre-existing CSV result outputs generated during Phases 5 and 6. Data was loaded and processed programmatically via Python (`src/analysis/analyze_results.py`) to prevent manual transcription errors. 

## Statistical Calculations
To evaluate the stochastic variability of the Genetic Algorithm, five independent experimental runs were performed on each dataset. For each metric, the mathematical Mean, Median, Minimum, Maximum, and Standard Deviation were calculated. Relative percentage improvements and absolute percentage point changes were computed using the Baseline algorithm's single deterministic run as the control value. Statistical significance testing (e.g., T-tests, ANOVA) was intentionally omitted, as five independent runs are sufficient to observe descriptive variance but generally insufficient to establish robust statistical significance without assuming normal distribution.

## Visualization Methodology
Visualizations were generated programmatically using `matplotlib` (`src/analysis/create_figures.py`). The charts compare the Baseline deterministic value against the GA's calculated mean across the 5 runs.
- **Figure 11 Limitation:** Generational convergence curves (Figure 11) were omitted because the complete `best_fitness_history` arrays were not logged to the final CSV outputs during the Phase 6 execution to conserve memory and file size. Reproducing this chart would require rerunning the experiments, which violates the strict Phase 7 constraints against modifying or rerunning the codebase.

## Data Sources
All analysis originates exclusively from the following files:
- `results/comparison/all_runs.csv`
- `results/comparison/comparison_results.csv`
- `results/experiments/*_results.csv`

## Reproducibility
The analysis is 100% reproducible. The Python scripts dynamically read the CSV files and execute the calculations and plot generation identically on every run. 

## Limitations
The analysis assumes the integrity of the underlying synthetic datasets. It was discovered that a significant portion of the Medium and Large dataset requirements were mathematically unallocatable. Consequently, the "Allocated Courses" comparisons represent the algorithm's performance on the *physically feasible subset* of the data, not the absolute total.
