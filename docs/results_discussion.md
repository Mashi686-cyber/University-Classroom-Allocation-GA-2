# Results and Discussion

## 1. Experimental Overview
This study evaluates a Genetic Algorithm (GA) against a sequential greedy heuristic (Baseline) for the classroom allocation problem. Experiments were conducted on three generated synthetic datasets: Small (20 courses), Medium (50 courses), and Large (100 courses). The GA was configured with a Population Size of 50, Crossover Rate of 0.8, Mutation Rate of 0.1, and an Elitism size of 2 based on preliminary One-Factor-At-A-Time (OFAT) parameter testing. To capture stochastic variability, the GA was executed across five independent random seeds (42, 43, 44, 45, 46) for each dataset. Performance was evaluated based on total conflicts (hard constraints), classroom utilization (soft objective), allocated courses, and execution time.

## 2. RQ1 — Conflict Reduction
**Results:** The experimental data indicates that the GA is highly effective at reducing conflicts. On both the Small and Medium datasets, the GA completely eliminated all conflicts (from 8 and 5 baseline conflicts, respectively, down to a mean of 0). On the Large dataset, the GA achieved a 91.4% mean conflict reduction (from 7 baseline conflicts down to a mean of 0.6).
**Trends & Reasons:** The sequential baseline lacks backtracking mechanisms, leading inevitably to overlapping lecturer schedules when the problem density increases. Conversely, the GA’s evolutionary search, guided by severe penalty weights for conflicts (-10,000), systematically navigates away from global overlaps.
**Limitations:** The GA did not achieve absolute zero conflicts on every single run for the Large dataset within the 50-generation limit, indicating that massive search spaces can still trap the algorithm in local optima.

## 3. RQ2 — Classroom Utilization
**Results:** The results suggest that the GA is capable of optimizing classroom utilization, but this behavior is subject to constraint boundaries. 
**Behavior by Dataset:**
- **Small Dataset:** Utilization decreased marginally by -0.1% (71.0% to 70.9%). The algorithm sacrificed a fraction of utilization to escape the 8 massive baseline conflicts.
- **Medium Dataset:** The GA improved utilization from 53.6% to 61.1% (+14.1% relative change).
- **Large Dataset:** The GA improved utilization from 63.2% to 68.9% (+8.9% relative change).
**Trade-offs:** Because the fitness function mathematically prioritizes hard constraints, the GA will actively choose a less mathematically "efficient" room if it is the only way to avoid a lecturer or student conflict. Both algorithms allocated the exact same number of courses across all datasets, meaning the GA's utilization improvements on Medium/Large are genuine efficiency gains, not artifacts of allocating fewer classes.

## 4. RQ3 — Parameter Effects
**Population Size:** Within the tested configurations, a population of 50 provided the best balance. Larger populations (200) converged in fewer generations but incurred unnecessary computational overhead.
**Generations:** The GA exhibited rapid convergence behavior on the tested datasets. The majority of fitness improvements occurred before generation 25, suggesting that extending runs to 500 generations provides diminishing returns given the current penalty structures.
**Mutation & Crossover:** A crossover rate of 0.8 facilitated the fastest convergence. Lower mutation rates (0.01 - 0.10) successfully maintained population diversity, while an excessively high mutation rate (0.20) became actively destructive, delaying convergence and reducing final utilization.
**Trade-offs:** These parameter effects indicate that the GA requires relatively lightweight configuration to solve the Small dataset. However, because multiple parameter configurations reached identical final fitness scores, the Small dataset is likely saturated for this algorithm.

## 5. RQ4 — Baseline vs GA
**Advantages of GA:** The GA heavily outperforms the baseline in producing feasible timetables. It reduced total conflicts by 91%-100% across all evaluated datasets and improved utilization by ~9-14% on the larger workloads without dropping course allocations.
**Disadvantages of GA:** The primary cost of the GA is computational execution time. The baseline executes in under 0.01 seconds, whereas the GA's mean execution time scales from 0.32s (Small) to 1.16s (Large). Additionally, the GA's stochastic nature means perfect allocations are not guaranteed within a fixed generation limit, as evidenced by the occasional remaining conflicts on the Large dataset.

## 6. Unexpected Findings
**Physically Infeasible Courses:** A significant portion of the generated courses were physically impossible to allocate (3 in Small, 14 in Medium, 49 in Large) due to the random synthesis of capacity and facility requirements. This created an artificial ceiling on the "Allocated Courses" metric for both algorithms.
**Large Dataset Variability:** The five Large-dataset GA seeds produced varying final states (Seeds 44 and 46 achieved 0 conflicts; Seeds 42, 43, 45 retained 1 conflict). This confirms that a 100-course problem size introduces enough combinatorial complexity to trap the search in local optima within 50 generations.

## 7. Limitations
The findings of this research must be interpreted within the context of several limitations:
1. **Synthetic Datasets**: The experiments rely on artificially generated data, which may not perfectly model the idiosyncratic nuances of real-world educational institutions.
2. **Lack of Real University Timetable Data**: True empirical validation against a historical, manually created university timetable is absent.
3. **Physically Infeasible Courses**: The synthetic generation produced an increasingly high volume of physically unallocatable courses (Small: 3, Medium: 14, Large: 49), capping the mathematical potential of the algorithms.
4. **Limited Dataset Sizes**: Evaluation was restricted to three discrete problem sizes (up to 100 courses), limiting the extrapolation of scalability claims.
5. **Limited Number of GA Seeds**: Five random seeds provide a baseline measure of stochastic variance but are insufficient for definitive confidence intervals.
6. **Limited Parameter Combinations**: Hyperparameter tuning was conducted using an OFAT approach rather than a comprehensive grid or random search.
7. **Large Dataset Conflict Variability**: The stochastic search occasionally became trapped in local optima on the Large dataset, failing to resolve the final remaining conflict within the generation limit.
8. **Missing Convergence History**: Complete generation-by-generation fitness histories were not stored during Phase 6, precluding the plotting of exact convergence trajectories (Figure 11).
9. **Execution Environment Dependency**: The reported sub-second execution times are strictly dependent on the underlying hardware architecture and Python interpreter speed used for this study.
10. **No Statistical Significance Testing**: Because of the limited seed count and lack of distribution normality checks, formal statistical significance claims (e.g., p-values) were not derived.

## 8. Overall Interpretation
Within the evaluated datasets and tested configurations, the experiments indicate that the Genetic Algorithm is a highly viable approach for classroom allocation. While it demands greater computational resources and is subject to stochastic variability, its ability to systematically navigate and resolve global timetable conflicts provides a substantial qualitative advantage over sequential heuristic scheduling.
