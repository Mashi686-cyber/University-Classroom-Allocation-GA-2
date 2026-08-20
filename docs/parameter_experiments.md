# Phase 5: Genetic Algorithm Parameter Experiments

## 1. Research Question (RQ3)
"What are the effects of various Genetic Algorithm parameters on classroom allocation?"
The goal of this phase is to systematically investigate how varying Population Size, Generations, Mutation Rate, and Crossover Rate affect the GA's ability to find feasible schedules and optimize utilization.

## 2. Experimental Methodology
Controlled experiments were performed on the **SMALL dataset** (20 courses, 10 classrooms, 20 timeslots). 
To isolate the effect of each parameter, a "One-Factor-At-A-Time" (OFAT) approach was utilized. Only the parameter under investigation was varied while all others were held at their baseline values.

## 3. Controlled Variables (Baseline)
- Population Size = 50
- Generations = 100
- Crossover Rate = 0.8
- Mutation Rate = 0.1
- Elitism = 2
- Random Seed = 42

*Note: The SMALL dataset contains 3 mathematically unallocatable courses due to synthetic constraints. Thus, the theoretical maximum fitness revolves around -300,000 (3 unallocated).*

## 4. Population-Size Experiment
**Tested Values:** [25, 50, 100, 200]
**Held Constant:** Gen=100, Cross=0.8, Mut=0.1, Seed=42

**Observations:**
- The algorithm consistently achieved a final fitness of `-299929.01` (Utilization `70.99%`) across all population sizes.
- **Trend**: Larger population sizes converge in fewer generations (Pop 25: Gen 48 -> Pop 200: Gen 15).
- **Trade-off**: The faster generation convergence comes at a steep computational cost. Execution time scales linearly with population size (0.31s to 2.40s). Pop 50 appears to be the sweet spot.

## 5. Generation Experiment
**Tested Values:** [50, 100, 200, 500]
**Held Constant:** Pop=50, Cross=0.8, Mut=0.1, Seed=42

**Observations:**
- Because the seed (42) and other parameters were fixed, the algorithm followed an identical search path in early generations, discovering the best-observed solution at Generation 23.
- **Trend**: Running beyond Generation 50 provided strictly zero benefit for this dataset while scaling execution time linearly (0.33s for 50 gen, up to 3.13s for 500 gen).
- **Unexpected Behavior**: The early stopping mechanism did not trigger because it checks for `fitness > 0`, which is mathematically impossible on the SMALL dataset due to the 3 unallocatable courses.

## 6. Mutation Experiment
**Tested Values:** [0.01, 0.05, 0.10, 0.20]
**Held Constant:** Pop=50, Gen=100, Cross=0.8, Seed=42

**Observations:**
- Mutation rates of 0.01, 0.05, and 0.10 all performed excellently, converging around Generation 22-24.
- **Unexpected Behavior (Worst Config)**: The high mutation rate of 0.20 proved destructive. It took until Generation 53 to find its best solution, and the final solution was slightly worse in utilization (`70.45%` instead of `70.99%`). High mutation disrupted the convergence of good building blocks.

## 7. Crossover Experiment
**Tested Values:** [0.60, 0.70, 0.80, 0.90]
**Held Constant:** Pop=50, Gen=100, Mut=0.1, Seed=42

**Observations:**
- Higher crossover rates generally improved convergence speed up to a point.
- Crossover `0.60` took 37 generations to converge, whereas `0.80` took only 23 generations. `0.90` was slightly slower (28 gen).
- **Best Config**: `0.80` provided the most effective balance between exploitation and exploration for this dataset.

## 8. Evaluation Metrics
The following metrics were tracked for each configuration:
- Final Fitness
- Allocated vs Unallocated Courses
- Hard Constraint Violations (Capacity, Room Type, Lecturer Conflicts, etc.)
- Classroom Utilization (%)
- Execution Time (seconds)
- Best Generation (generation at which the best solution was found)

## 9. Reproducibility
All experiments utilized a fixed seed (`random.seed(42)`). The `parameter_experiments.py` runner automatically resets the seed at the start of each individual configuration run, guaranteeing absolute reproducibility. Rerunning the script yields identical results byte-for-byte.

## 10. Limitations
- These initial parameter experiments were performed exclusively on the SMALL dataset to establish a baseline behavior profile. The behavior (and optimal parameters) may shift dramatically for the highly constrained LARGE dataset due to exponential increases in search space size.
- A full Grid Search or Random Search of the hyperparameter space was not performed to prevent combinatorial explosion; OFAT testing cannot capture complex interaction effects between parameters (e.g., high mutation + high crossover).
