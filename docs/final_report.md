# University Classroom Allocation Optimization Using Genetic Algorithm

BSc (Hons) in Information Technology

Nature Inspired Algorithm
IT41033

Group Members:
[Student Name 1] – [Student Index Number]
[Student Name 2] – [Student Index Number]
[Student Name 3] – [Student Index Number]

Submission Date:
2026

---

## ABSTRACT

The allocation of university classrooms is a highly constrained scheduling problem that becomes increasingly difficult to solve manually as student enrollment and course offerings grow. Sequential heuristic methods often fail to resolve interdependent constraints, resulting in double-booked lecturers, student group overlap, and inefficient use of physical space. This research proposes an automated classroom allocation system optimized by a Genetic Algorithm (GA) to minimize scheduling conflicts and maximize classroom utilization. Due to the unavailability of comprehensive real-world institutional data, reproducible synthetic datasets of three scales (Small, Medium, Large) were generated to model complex interdependencies such as classroom capacities, facility requirements, and multi-slot course durations. The proposed GA utilizes Tournament Selection, Uniform Crossover, and Resetting Mutation, driven by a penalty-based fitness hierarchy that strictly prioritizes hard constraints over soft utilization objectives. The performance of the GA was benchmarked against a deterministic, greedy first-fit baseline heuristic. The experimental results demonstrate that the GA successfully reduces total conflicts by 100% on Small and Medium datasets and 91.4% on Large datasets, significantly outperforming the baseline. Furthermore, the GA achieved a relative utilization increase of up to +14.1% on larger problem spaces. While the algorithm requires moderately higher computational execution time and is subject to stochastic variability in massive search spaces, the findings indicate that evolutionary optimization provides a substantially superior and viable approach for university classroom scheduling under the evaluated conditions.

---

## 1. INTRODUCTION

University classroom allocation is a foundational administrative task that requires assigning academic courses to specific physical spaces and timeslots. As academic institutions expand their curricula and student intake, the complexity of this scheduling task increases exponentially. The process is governed by strict physical and temporal constraints: classrooms must have adequate capacity, specific room types (e.g., laboratories vs. lecture halls), and required multimedia facilities. Concurrently, temporal constraints dictate that no lecturer can teach two classes simultaneously, nor can a single student group attend overlapping courses. 

When human administrators or simple sequential computer programs attempt to solve this problem, they typically process courses one by one. This often leads to a "conflict cascade," where assigning an optimal room early in the process inadvertently creates impossible constraints for courses scheduled later, ultimately resulting in scheduling conflicts or poorly utilized classroom space. 

Because classroom allocation belongs to a class of highly complex, NP-hard combinatorial problems, traditional computational methods struggle to find viable solutions efficiently [4]. To address this, researchers often turn to optimization techniques, particularly Nature-Inspired Algorithms [3]. A Genetic Algorithm (GA) is a prominent evolutionary technique inspired by biological natural selection [1]. By mimicking the processes of reproduction, crossover, and mutation, a GA evaluates multiple potential timetables simultaneously, gradually evolving them to satisfy complex global constraints [2]. The purpose of this research is to investigate the efficacy of applying a Genetic Algorithm to resolve the university classroom allocation problem, minimizing schedule conflicts while optimizing physical space utilization.

---

## 2. BACKGROUND

### 2.1 University Timetabling
University timetabling encompasses the organization of educational events (lectures, exams) within limited temporal and physical resources. It is widely recognized as a complex optimization challenge due to the immense number of possible combinations [4], [5].

### 2.2 Classroom Allocation
Classroom allocation specifically focuses on matching courses to appropriate physical rooms once general time windows are established, or assigning both room and time simultaneously to ensure no physical or human resources overlap.

### 2.3 Constraints in Classroom Allocation
Constraints are typically divided into two categories:
- **Hard Constraints**: Rules that cannot be broken under any circumstances for a timetable to be physically feasible (e.g., a room cannot hold more students than its capacity; a lecturer cannot be in two places at once).
- **Soft Constraints (Objectives)**: Preferences that should be optimized but do not invalidate the timetable if unmet (e.g., packing classrooms efficiently so that large rooms are not wasted on small classes).

### 2.4 Optimization Problems
An optimization problem involves searching through a vast landscape of possible solutions to find the one that best minimizes a cost function or maximizes a reward function, without explicitly checking every single possibility.

### 2.5 Nature-Inspired Algorithms
Nature-Inspired Algorithms are metaheuristic optimization strategies based on biological or physical phenomena (e.g., swarm intelligence, evolutionary biology) designed to navigate massive, complex search spaces efficiently [3].

### 2.6 Genetic Algorithms
A Genetic Algorithm is a specific evolutionary approach containing the following components:
- **Population**: A collection of potential solutions.
- **Chromosome**: The mathematical representation of a single complete solution (a full university timetable).
- **Gene**: A specific variable within the chromosome (a single course assignment).
- **Fitness**: A scoring function evaluating how good a solution is based on constraint violations.
- **Selection**: The process of choosing high-fitness solutions to reproduce.
- **Crossover**: Combining parts of two parent solutions to create a new offspring timetable.
- **Mutation**: Randomly altering a small part of a solution to introduce new genetic diversity.
- **Elitism**: Directly preserving the absolute best solutions across generations to prevent regression.
- **Termination**: The condition under which the algorithm stops searching (e.g., reaching a maximum number of generations).

---

## 3. PROBLEM STATEMENT

Manual university classroom allocation is an exceedingly difficult and error-prone administrative burden. As the number of offered courses increases, the likelihood of scheduling conflicts rises dramatically. Administrators frequently encounter lecturer conflicts (double-booking a professor) and student-group conflicts (forcing students to choose between mandatory overlapping classes). Furthermore, manual allocation often results in capacity mismatch—placing small classes in large lecture halls—which leads to poor institutional space utilization. 

A simple computational approach, such as assigning rooms on a first-come, first-served basis, is insufficient because it cannot backtrack to resolve interdependent bottlenecks. Therefore, a robust computational optimization approach is required to systematically evaluate the global impact of every assignment, effectively minimizing timetable conflicts and maximizing the utility of existing physical infrastructure.

---

## 4. RESEARCH QUESTIONS AND OBJECTIVES

This study is driven by the following four research questions:
- **RQ1**: Is it possible to use Genetic Algorithm in reducing the conflicts in classroom allocation in universities?
- **RQ2**: Is it possible to optimize the usage of the existing classrooms in universities through Genetic Algorithm?
- **RQ3**: What are the effects of various Genetic Algorithm parameters on classroom allocation?
- **RQ4**: Does the Genetic Algorithm-based classroom allocation approach outperform the simple classroom allocation approach?

**Primary Objective**: 
To build and evaluate a research-quality University Classroom Allocation Optimization System utilizing a Genetic Algorithm.

**Specific Objectives**:
1. To design a reproducible dataset representing complex university scheduling constraints.
2. To implement a baseline sequential allocation algorithm for comparative analysis.
3. To develop a Genetic Algorithm incorporating hierarchical constraint-based fitness evaluation.
4. To experimentally determine the impact of evolutionary parameters on convergence and fitness.
5. To compare the algorithmic outcomes based on conflict reduction, utilization, and execution efficiency.

---

## 5. DATASET

The acquisition of real-world, highly constrained university classroom allocation datasets is challenging due to privacy regulations and formatting inconsistencies. While public datasets (such as those found on Kaggle) were initially inspected, they lacked the complete physical topologies—such as matching classroom facility arrays to course requirements—necessary to test a rigorous multi-constraint optimization engine.

Therefore, a reproducible, relational synthetic dataset generator was engineered. The generation methodology enforces realistic relationships: courses strictly belong to defined student groups, lecturers are constrained to normal teaching loads, and classrooms possess specific capacities, types, and multimedia facilities. To ensure absolute experimental reproducibility, the generator utilizes a fixed random seed (`42`). 

The generated dataset is structured into five distinct entities:
- **Courses**: Contains ID, Student Group, Lecturer, Students, Room Type, Facilities, and Duration.
- **Classrooms**: Contains ID, Capacity, Room Type, Facilities, and Availability schedule.
- **Lecturers**: Contains unique Lecturer IDs.
- **Student Groups**: Contains cohort identifiers.
- **Time Slots**: Contains standardized time blocks across the academic week.

---

## 6. DATASET CONFIGURATIONS

The generator was configured to produce three distinct dataset scales to evaluate algorithm performance under increasing complexity:

| Dataset | Courses | Student Groups | Lecturers | Classrooms | Time Slots |
|---|---|---|---|---|---|
| Small | 20 | 10 | 10 | 10 | 20 |
| Medium | 50 | 10 | 20 | 15 | 25 |
| Large | 100 | 10 | 35 | 20 | 30 |

Because the dataset was generated using random constraint synthesis, a structural limitation emerged: a subset of courses demanded physical requirements (e.g., specific facility combinations coupled with massive capacities) that no generated classroom possessed. Specifically, 3 courses in the Small dataset, 14 in the Medium dataset, and 49 in the Large dataset were fundamentally physically infeasible. It is crucial to distinguish this absolute physical feasibility from global timetable feasibility (conflicting overlaps). This physical cap represents the maximum theoretical allocation limit for any algorithm operating on these synthetic files.

---

## 7. DATA PREPROCESSING AND VALIDATION

To ensure data integrity prior to algorithmic execution, a stringent programmatic validation pipeline was applied to the generated CSV files. The validation scripts performed:
- Missing-value checking across all fields.
- Duplicate identification.
- Foreign-key referential validation (ensuring every course referenced a valid lecturer and student group).
- Physical constraint validation (ensuring capacities were positive integers and durations were valid).
- Array decoding validation (parsing JSON-encoded facility arrays).

All three generated datasets (Small, Medium, Large) passed validation with zero errors, confirming that the algorithmic evaluation would operate on structurally sound relational data.

---

## 8. BASELINE ALGORITHM

To establish a comparative benchmark for RQ4, a deterministic baseline algorithm was implemented. The baseline relies on a sequential, greedy first-fit heuristic. 

**Algorithm Steps:**
1. Process courses sequentially.
2. Search available classrooms in a fixed deterministic order.
3. Check hard physical capacities (Capacity, Room Type, Facilities).
4. Search available contiguous timeslots matching the course duration.
5. Select the first suitable assignment that does not conflict with the room's schedule.
6. Continue to the next course without any global backtracking.

This baseline was selected because it closely mimics the standard, non-computational human approach to scheduling: resolving immediate problems without foresight. Its primary limitation is its inability to retrospectively alter a valid placement to resolve a massive conflict occurring later in the queue. It is not an inherently flawed algorithm; rather, it represents the standard heuristic ceiling that advanced optimization models attempt to surpass.

---

## 9. GENETIC ALGORITHM DESIGN

### 9.1 Chromosome Representation
The schedule is represented as a single chromosome consisting of multiple genes. Each gene corresponds to a course, containing a tuple of `(Classroom_ID, Time_Slot_Window)`. To successfully handle courses requiring multiple hours, the `Time_Slot_Window` is formulated as a continuous block of consecutive timeslots, ensuring multi-hour courses are never fragmented across different days.

### 9.2 Initial Population
The initial population is generated by creating random course-to-room assignments. The initialization process includes a basic physical filter to ensure the GA does not waste generations evaluating mathematically impossible room assignments. The random initialization uses seed `42` to guarantee deterministic reproducibility across runs.

### 9.3 Fitness Function
The fitness function utilizes a hierarchical penalty structure to strictly enforce constraints.
- **Unallocated Penalty**: `-100,000` per unallocated course.
- **Conflict Penalty**: `-10,000` for every lecturer, student-group, or classroom overlapping conflict.
- **Utilization Reward**: `+0` to `+100` added based on the calculated percentage of classroom utilization.

This exact mathematical hierarchy ensures that the algorithm can never improve its score by increasing classroom utilization at the expense of introducing a scheduling conflict.

### 9.4 Selection
The GA uses Tournament Selection. A subset of individuals (default size of 3) is randomly chosen, and the individual with the highest fitness is selected to become a parent, ensuring strong evolutionary pressure while maintaining genetic diversity.

### 9.5 Crossover
Uniform Crossover is utilized. For each gene (course), there is a probability that the offspring will inherit the assignment from Parent A or Parent B, allowing the algorithm to seamlessly mix optimal sub-schedules from different timetables.

### 9.6 Mutation
Resetting Mutation is applied. Under a specific probability, a gene's assignment is entirely discarded and replaced with a newly randomized, physically valid `(Classroom, Time_Slot_Window)` tuple. This introduces fresh genetic material to prevent the population from stagnating.

### 9.7 Elitism
The algorithm implements elitism by directly copying the top 2 best-performing chromosomes from the current generation into the next generation. This guarantees that the highest-achieved fitness is never lost due to destructive mutation.

### 9.8 Termination
The algorithm terminates when it reaches a predefined maximum number of generations (default 50), after which the single best chromosome from the final generation is returned as the solution.

---

## 10. CONSTRAINTS AND EVALUATION

To guarantee unbiased evaluation, both the Baseline and GA share identical programmatic evaluation rules:
- **Classroom Conflict**: Two distinct courses placed in the same room at the same time.
- **Lecturer Conflict**: A lecturer scheduled to teach two different classes at the same time.
- **Student-Group Conflict**: A student cohort scheduled for two different classes at the same time.
- **Capacity Violation**: Course enrollment exceeds room capacity.
- **Facility / Room-Type Violation**: Room lacks requested physical characteristics.
- **Availability Violation**: Room is occupied or closed.
- **Unallocated Course**: A course left without a valid room/time tuple.

Classroom utilization is evaluated as a soft objective using the exact implemented formula:
`Overall Utilization = (Total Student Slot-Hours Assigned / Total Capacity Slot-Hours Available) * 100`

---

## 11. EXPERIMENTAL METHODOLOGY

The experimental evaluation was conducted in distinct phases. First, a baseline experiment was executed deterministically on all three datasets. Second, a parameter experiment was conducted using a One-Factor-At-A-Time (OFAT) methodology to isolate hyperparameter effects. 

Finally, the main GA experiment was executed across the Small, Medium, and Large datasets. To accurately assess the stochastic nature of evolutionary algorithms, the GA was run using five independent random seeds (`42, 43, 44, 45, 46`). The main experiment configuration used the values identified during the parameter trials: Population = 50, Generations = 50, Crossover = 0.80, Mutation = 0.10, and Elitism = 2.

---

## 12. PARAMETER EXPERIMENTS

The Phase 5 OFAT parameter trials were conducted exclusively on the Small dataset.
- **Population Size (25, 50, 100, 200)**: A population of 50 achieved the maximum possible fitness (-299,929.01) efficiently. Larger populations (200) increased execution time linearly with no corresponding benefit in final fitness.
- **Generations (50, 100, 200, 500)**: The algorithm rapidly converged before generation 25. Executing beyond 50 generations yielded 0 improvement.
- **Mutation (0.01, 0.05, 0.10, 0.20)**: While lower rates maintained diversity, an aggressively high mutation rate of 0.20 proved destructive, actively dragging final fitness down to -299,936.56.
- **Crossover (0.60, 0.70, 0.80, 0.90)**: A rate of 0.80 provided the most rapid convergence.

These parameter results indicate a degree of saturation on the Small dataset, meaning the parameters are highly effective under these tested conditions but are not claimed to be globally optimal for massively scaled environments.

---

## 13. RESULTS

The following data summarizes the empirical performance metrics derived directly from the experimental outputs.

### 13.1 Baseline Results
The deterministic baseline successfully allocated all physically feasible courses (17 Small, 36 Medium, 51 Large). It executed in under 0.01 seconds across all runs but produced substantial total conflicts (8 Small, 5 Medium, 7 Large). 

### 13.2 GA Results
The GA algorithm successfully allocated the exact same number of physically feasible courses. 

### 13.3 Small Dataset
- Baseline Total Conflicts: 8
- GA Mean Total Conflicts: 0
- Baseline Utilization: 71.0%
- GA Mean Utilization: 70.9%

### 13.4 Medium Dataset
- Baseline Total Conflicts: 5
- GA Mean Total Conflicts: 0
- Baseline Utilization: 53.6%
- GA Mean Utilization: 61.1%

### 13.5 Large Dataset
- Baseline Total Conflicts: 7
- GA Mean Total Conflicts: 0.6
- Baseline Utilization: 63.2%
- GA Mean Utilization: 68.9%

### 13.6 Five-Seed Variability
The five stochastic runs on the Large dataset demonstrated slight variability in resolving the final conflict. Two runs (Seeds 44, 46) achieved a perfect 0 conflict state, while three runs (Seeds 42, 43, 45) terminated at generation 50 with 1 residual conflict.

### 13.7 Execution Time
Mean GA execution time scaled upward with problem complexity: 0.32s for Small, 0.72s for Medium, and 1.16s for Large.

### 13.8 Classroom Utilization
See `results/figures/fig02_utilization_comparison.png`.

### 13.9 Conflict Reduction
See `results/figures/fig01_conflict_comparison.png`.

---

## 14. RESEARCH QUESTION ANALYSIS

### 14.1 RQ1 — Conflict Reduction
The evidence indicates that the Genetic Algorithm is exceptionally capable of reducing classroom allocation conflicts. By prioritizing penalty avoidance, the GA reduced total conflicts by 100% on the Small and Medium datasets, and by 91.4% on the Large dataset. 

### 14.2 RQ2 — Classroom Utilization
The GA optimized the usage of existing classrooms effectively on broader datasets. On the Medium dataset, utilization improved by +7.5 percentage points (+14.1% relative change). On the Large dataset, utilization improved by +5.7 percentage points (+8.9% relative change). Conversely, the Small dataset saw a minor decrease of -0.1 percentage points (-0.2% relative change), demonstrating the GA's programmed willingness to sacrifice soft objectives to resolve hard conflicts.

### 14.3 RQ3 — Parameter Effects
Parameter evaluations suggest that within this specific algorithmic architecture, high crossover rates (0.80) coupled with moderate population sizes (50) drive rapid generation convergence. Furthermore, execution time scaled directly with population size and generation limits, emphasizing that careful parameter tuning is required to balance computational cost against evolutionary exploration. High mutation rates were observed to be actively detrimental to finalizing stable timetables.

### 14.4 RQ4 — Baseline vs GA
The Genetic Algorithm heavily outperforms the simple baseline heuristic in timetable quality. While both algorithms allocated the exact same feasible course load, the GA virtually eliminated overlapping constraint violations and generated tighter room-packing efficiencies. The sole metric where the baseline outperformed the GA was execution time (instantaneous vs ~1.16s), a negligible trade-off given the severity of the scheduling conflicts resolved by the GA.

---

## 15. DISCUSSION

The experimental results validate the core hypothesis of evolutionary scheduling algorithms: sequential allocation fails because it lacks the capacity to retroactively adjust earlier assignments to accommodate complex bottlenecks. The greedy baseline inadvertently triggered overlapping lecturer and student schedules because it greedily consumed the first available timeslot. By contrast, the GA evaluated the timetable globally, systematically exchanging genes to resolve overlaps.

The minor utilization decrease observed on the Small dataset perfectly illustrates the success of the fitness hierarchy. The baseline achieved a slightly higher utilization by illegally double-booking lecturers (8 conflicts). The GA detected these conflicts and absorbed massive -10,000 point penalties. To resolve them, it moved classes to slightly less mathematically optimal rooms, trading a fraction of a percent of utilization to achieve a legally feasible schedule. 

The appearance of unallocated courses (3, 14, 49) across both algorithms highlights the physical boundaries of the generated datasets, wherein courses simply possessed required capacities and facilities that did not exist within the available classrooms. Additionally, the variability of the Large dataset results (leaving an average of 0.6 conflicts) confirms that as the search space grows, the standard 50-generation limit becomes occasionally insufficient to escape deep local optima.

---

## 16. LIMITATIONS

The findings of this research must be interpreted within the context of the following limitations:
1. **Synthetic Datasets**: The experiments rely on artificially generated data, which may not perfectly model the idiosyncratic nuances of real-world educational institutions.
2. **Lack of Real University Timetable Data**: True empirical validation against a historical, manually created university timetable is absent.
3. **Physically Infeasible Courses**: The synthetic generation produced an increasingly high volume of physically unallocatable courses, capping the mathematical potential of the algorithms.
4. **Limited Dataset Sizes**: Evaluation was restricted to three discrete problem sizes, limiting the extrapolation of massive scalability claims.
5. **Limited Number of Random Seeds**: Five random seeds provide a baseline measure of stochastic variance but are insufficient for definitive statistical confidence intervals.
6. **Limited Parameter Combinations**: Hyperparameter tuning was conducted using an OFAT approach rather than a comprehensive grid or random search.
7. **Large Dataset Conflict Variability**: The stochastic search occasionally became trapped in local optima on the Large dataset.
8. **Missing Phase 6 Convergence History**: Complete generation-by-generation fitness histories were not stored during Phase 6, precluding the exact analysis of evolutionary trajectories in the largest environments.
9. **Execution Environment Dependency**: The reported sub-second execution times are dependent on the specific underlying hardware and Python interpreter used for this study.
10. **No Formal Statistical Significance Testing**: Because of the limited seed count, formal significance testing (e.g., ANOVA, T-tests) was not conducted.
11. **Synthetic Data Assumptions**: The assumption that facilities and capacities are entirely rigid hard constraints may not reflect flexible real-world administrative overrides.

---

## 17. ETHICAL AND PRACTICAL CONSIDERATIONS

Because the research utilizes fully synthetic data generation, no personal student, lecturer, or institutional privacy data was compromised. From a practical standpoint, the developed system is intended as an automated decision-support tool rather than an autonomous dictator of university policy. Before any algorithmically generated schedule is deployed in a real university setting, it must be subject to rigorous manual review by human administrators to account for un-coded human constraints and institutional preferences.

---

## 18. CONCLUSION

This research successfully addressed the highly complex problem of university classroom allocation by developing and evaluating a Genetic Algorithm framework. Under the tested datasets and configurations, the Genetic Algorithm demonstrated substantial superiority over a standard sequential heuristic allocation method. Guided by a strict hierarchical penalty system, the GA reduced severe scheduling conflicts by over 91% across all datasets and achieved relative utilization efficiency gains of up to 14.1% in larger environments. While limited by the boundaries of synthetic dataset generation and bounded computational exploration, the empirical evidence confirms that evolutionary algorithms represent a highly effective and viable computational methodology for resolving multidimensional university timetabling constraints.

---

## 19. FUTURE WORK

Future research should focus on validating the algorithm against actual historical university datasets to confirm its real-world applicability. Additionally, the synthetic data generator should be enhanced to guarantee baseline physical feasibility for all generated courses. From an algorithmic perspective, developing a multi-objective GA (e.g., NSGA-II) could allow for a more nuanced Pareto-front analysis between conflicting objectives. Finally, incorporating a hybrid local-search mechanism (Memetic Algorithm) could help the system reliably escape the local optima observed during the Large dataset evaluations.

---

## 20. REFERENCES

[1] J. H. Holland, *Adaptation in Natural and Artificial Systems*, 2nd ed. Cambridge, MA, USA: MIT Press, 1992.
[2] D. E. Goldberg, *Genetic Algorithms in Search, Optimization, and Machine Learning*. Reading, MA, USA: Addison-Wesley, 1989.
[3] X.-S. Yang, *Nature-Inspired Optimization Algorithms*, 2nd ed. London, UK: Academic Press, 2020.
[4] A. Schaerf, "A survey of automated timetabling," *Artificial Intelligence Review*, vol. 13, no. 2, pp. 87–127, 1999.
[5] E. K. Burke, J. P. Newall, and R. F. Weare, "A memetic algorithm for university exam timetabling," in *Practice and Theory of Automated Timetabling*, Springer, 1996, pp. 241–250.

---

## 21. APPENDICES

- **Appendix A**: Dataset schema mappings and definitions (`docs/dataset_design.md`).
- **Appendix B**: Genetic Algorithm configuration architectures (`docs/ga_design.md`).
- **Appendix C**: Experimental OFAT parameter ranges (`docs/parameter_experiments.md`).
- **Appendix D**: Full result tables (`results/analysis/`).
- **Appendix E**: Software evaluation object definitions (`docs/evaluation_definitions.md`).
- **Appendix F**: Scripts required to regenerate identical results (`README.md`).

---

## 22. FIGURE REFERENCES

- Figure 1: Conflict Comparison (`results/figures/fig01_conflict_comparison.png`)
- Figure 2: Utilization Comparison (`results/figures/fig02_utilization_comparison.png`)
- Figure 3: Allocated Courses (`results/figures/fig03_allocated_courses.png`)
- Figure 4: Execution Time (`results/figures/fig04_execution_time.png`)
- Figure 5: Population vs Fitness (`results/figures/fig05_population_fitness.png`)
- Figure 6: Population vs Execution Time (`results/figures/fig06_population_time.png`)
- Figure 7: Generations vs Fitness (`results/figures/fig07_generations_fitness.png`)
- Figure 8: Generations vs Time (`results/figures/fig08_generations_time.png`)
- Figure 9: Mutation Rate vs Fitness (`results/figures/fig09_mutation_fitness.png`)
- Figure 10: Crossover Rate vs Fitness (`results/figures/fig10_crossover_fitness.png`)
- Figure 11: *(Convergence History Omitted)*
- Figure 12: Large Dataset Five-Seed Variance (`results/figures/fig12_large_seed_analysis.png`)
