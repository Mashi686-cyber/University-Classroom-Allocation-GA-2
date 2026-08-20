# Phase 6: Corrective Audit

This document serves as a research-quality audit of the preliminary Phase 6 conclusions, validating physical feasibility, execution behavior, conflict reporting, and fitness priority.

## 1. Feasibility Findings
An independent physical feasibility analysis was conducted on the generated datasets to determine if at least one classroom existed satisfying the Capacity, Room Type, and Facilities requirements for every course.
- **Medium Dataset**: 50 total courses. 36 are physically feasible. 14 are physically infeasible (`C004, C005, C009, C015, C016, C018, C026, C027, C030, C032, C035, C037, C046, C050`).
- **Large Dataset**: 100 total courses. 51 are physically feasible. 49 are physically infeasible.
*Conclusion*: The number of unallocated courses observed in both the Baseline and GA precisely matches the count of physically infeasible courses. Therefore, the algorithms successfully allocated the physically capable load. The unallocated courses are a limitation of the synthetic dataset generation, not the algorithms. This distinguishes physical feasibility from global timetable feasibility (conflicts).

## 2. Large-Seed Findings & 3. Conflict Analysis
The Large dataset GA runs yielded a mean of 0.6 conflicts. A seed-by-seed audit reveals:
- **Seed 42**: 1 Student Group Conflict
- **Seed 43**: 1 Lecturer Conflict
- **Seed 44**: 0 Conflicts
- **Seed 45**: 1 Student Group Conflict
- **Seed 46**: 0 Conflicts
*Conclusion*: The GA does occasionally fail to resolve all global conflicts on the Large dataset within the 50-generation limit. The resulting mean is not an artifact; specific seeds (42, 43, 45) genuinely produced exactly 1 conflict each. 

## 4. Utilization Verification
The classroom utilization calculation was audited in `src/evaluation/metrics.py`. Both the Baseline and GA use the exact same calculation object.
The formula calculates:
`Overall Utilization = (Total Student Slot-Hours Assigned / Total Capacity Slot-Hours Available) * 100`
Course duration is explicitly factored into both the numerator and denominator by scaling the student count and classroom capacity by the length of the assigned timeslot window. 

## 5. Execution-Time Verification
Execution times from the Phase 6 results were recalculated to observe scaling behavior:
- **Small (20) → Medium (50)**: Dataset size increased by 2.5x. Mean GA execution time increased from 0.32s to 0.72s (a 2.25x increase).
- **Medium (50) → Large (100)**: Dataset size increased by 2.0x. Mean GA execution time increased from 0.72s to 1.16s (a 1.61x increase).
- **Small (20) → Large (100)**: Dataset size increased by 5.0x. Mean GA execution time increased from 0.32s to 1.16s (a 3.62x increase).
*Conclusion*: These observations strictly indicate the execution time increased as the dataset grew. The observed scaling factor (3.62x time for 5.0x data) is noted, but this is an empirical observation from three data points, not a formal complexity proof.

## 6. RQ1 Audit (Conflict Reduction)
The data strictly supports that the GA reduced conflicts relative to the baseline. It achieved a 100% reduction on the Small and Medium datasets, and a 91.4% reduction on the Large dataset (from 7 down to a 0.6 average).

## 7. RQ2 Audit (Classroom Utilization)
The data shows that the GA improved utilization on the Medium (53.6% → 61.1%) and Large (63.2% → 68.9%) datasets. However, utilization slightly decreased on the Small dataset (71.0% → 70.9%). Therefore, the GA does not universally improve utilization, but it optimizes it subject to the strict adherence to the hard constraints.

## 8. RQ3 Audit (Parameter Effects)
The OFAT experiments indicate that `Population=50` and `Crossover=0.8` were the most effective parameters *for the Small dataset*. Because the GA reliably hit the maximum possible fitness on nearly all configurations for the Small dataset, this suggests the Small problem space is relatively easy or saturated. These parameters are not claimed to be globally optimal for larger, more complex spaces.

## 9. RQ4 Audit (Algorithm Comparison)
The claim that the GA produces a "genuinely feasible timetable" for the Large dataset is inaccurate, as some seeds produced 1 remaining conflict. The corrected observation is that the GA significantly reduces conflicts (by >91%), optimizes utilization where mathematically permitted, and allocates identical numbers of courses to the baseline, at the cost of increased computational execution time (0.01s vs ~1.16s).

## 10. Fitness Validation
Explicit unit testing (`test_case_i_hard_constraint_dominates_utilization`) was written and verified to prove that:
1. Hard constraints mathematically dominate the utilization reward.
2. A solution with zero hard violations and minimum utilization will strictly evaluate to a higher fitness than a solution with one hard violation and maximum utilization. 
3. The GA's penalty hierarchy strictly enforces this rule.

## 11. Limitations
- The synthetic dataset generation produced heavily constrained physical environments, rendering nearly 50% of the Large dataset courses unallocatable regardless of the scheduling algorithm.
- Parameter optimization (RQ3) was only performed on the Small dataset.
- Five random seeds provide a measure of variability but are insufficient to claim robust statistical significance.
