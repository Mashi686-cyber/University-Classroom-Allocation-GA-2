# Baseline Classroom Allocation Method

## 1. Purpose of the Baseline
The baseline algorithm serves as a non-optimized, naive reference point. Its sole purpose is to represent a straightforward, manual or heuristic approach to classroom allocation that a university administrator might use without the aid of advanced optimization techniques. It provides a fair, lower-bound benchmark against which the subsequent Genetic Algorithm (GA) will be compared to answer the primary research questions regarding conflict reduction and utilization improvement.

## 2. Algorithm Steps
1. Deterministically load and sort the lists of courses, classrooms, and timeslots by their unique IDs.
2. Pre-calculate available continuous time windows for courses requiring multiple slots (e.g., Duration = 2).
3. Sequentially process each course one by one.
4. For each course, search for the first available classroom and time window combination that satisfies its physical requirements.
5. Record the allocation and mark the classroom's timeslot as occupied.
6. Continue to the next course without ever revisiting or modifying previous allocations.

## 3. Allocation Strategy
The strategy relies on a **greedy, first-fit heuristic**. It prioritizes satisfying hard physical constraints (Capacity, Room Type, Facilities) but blindly assigns timeslots without considering the global schedules of lecturers or student groups. If no matching classroom/time slot is found for a course, it is left unallocated. Crucially, the algorithm *never globally rearranges previous assignments* to fix newly discovered conflicts or improve utilization.

## 4. Constraints Checked
The system checks all allocations against the ground truth dataset and records violations.
- **Classroom conflict**: Same classroom scheduled multiple times in one slot (prevented by the greedy allocator itself, but checked in evaluation).
- **Lecturer conflict**: A lecturer scheduled to teach multiple courses at the same time.
- **Student group conflict**: A student group scheduled to attend multiple courses at the same time.
- **Capacity violation**: Number of students exceeds room capacity.
- **Facility mismatch**: Room lacks required facilities.
- **Room type mismatch**: Room is not the required type.
- **Availability violation**: Room scheduled during an unavailable time.
- **Unallocated courses**: Courses that failed to receive any assignment.

## 5. Metrics
The primary soft objective metric is **Classroom Utilization**.
- **Individual Utilization**: `(Number_of_Students / Classroom_Capacity) × 100` per course allocation.
- **Overall Utilization**: `(Total Students Assigned / Total Available Classroom Capacity Used) × 100`. (Weighted by duration).

## 6. Complexity
- **Time Complexity**: `O(C * R * T)`, where `C` is the number of courses, `R` is the number of classrooms, and `T` is the number of timeslots. It is extremely fast and executes in polynomial time.
- **Space Complexity**: `O(R * T)` to track the classroom schedule, plus `O(C)` to store the output allocations.

## 7. Limitations
- It is myopic; a poor early choice can block dozens of subsequent courses.
- It completely ignores lecturer and student group availability, leading to massive schedule conflicts.
- It does not attempt to maximize utilization (e.g., placing 10 students in a 150-capacity room is deemed "valid" if it's the first available fit).

## 8. Why this is an appropriate baseline
A genetic algorithm's true strength lies in navigating complex, interdependent constraints that are impossible to resolve sequentially. By using a strictly sequential, non-backtracking greedy algorithm, we simulate the "conflict cascade" that occurs in manual timetabling. Any reduction in lecturer/student group conflicts or improvements in capacity utilization achieved by the GA will thus demonstrate the optimization value of evolutionary search over basic heuristics.
