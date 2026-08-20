# Final Results Cross-Check

This document verifies the key numerical outputs presented in the final documentation against the generated `results/comparison/comparison_results.csv` and `results/comparison/summary.csv` files.

## 1. Small Dataset Check
- **Baseline**: Allocated: 17, Unallocated: 3, Conflicts: 8, Utilization: 71.0%, Execution Time: ~0.00s
- **GA (Mean)**: Allocated: 17, Unallocated: 3, Conflicts: 0, Utilization: 70.9%, Execution Time: ~0.32s
*Status*: MATCH. 

## 2. Medium Dataset Check
- **Baseline**: Allocated: 36, Unallocated: 14, Conflicts: 5, Utilization: 53.6%, Execution Time: ~0.00s
- **GA (Mean)**: Allocated: 36, Unallocated: 14, Conflicts: 0, Utilization: 61.1%, Execution Time: ~0.72s
*Status*: MATCH.

## 3. Large Dataset Check
- **Baseline**: Allocated: 51, Unallocated: 49, Conflicts: 7, Utilization: 63.2%, Execution Time: ~0.00s
- **GA (Mean)**: Allocated: 51, Unallocated: 49, Conflicts: 0.6, Utilization: 68.9%, Execution Time: ~1.16s
*Status*: MATCH.

## 4. Derived Metrics Check
- **RQ1 Conflict Reduction**: 
  - Small: 8 -> 0 = 100.0%
  - Medium: 5 -> 0 = 100.0%
  - Large: 7 -> 0.6 = 91.4%
*Status*: MATCH.

- **RQ2 Utilization Changes**:
  - Small: 71.0% -> 70.9% = -0.1 percentage points (-0.2% relative)
  - Medium: 53.6% -> 61.1% = +7.5 percentage points (+14.1% relative)
  - Large: 63.2% -> 68.9% = +5.7 percentage points (+8.9% relative)
*Status*: MATCH.

## 5. Conclusion
All manually typed metrics in the markdown documentation accurately reflect the programmatically generated CSV analysis files. No numerical contradictions were found.
