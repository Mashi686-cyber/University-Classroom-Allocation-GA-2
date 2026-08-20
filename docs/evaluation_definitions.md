# Evaluation Definitions

To guarantee an unbiased comparison, both the sequential Baseline algorithm and the Genetic Algorithm are evaluated using identical, shared programmatic objects (`ConstraintChecker` in `src/evaluation/constraint_checker.py` and `MetricsCalculator` in `src/evaluation/metrics.py`). 

## 1. Conflict Definitions (Hard Constraints)
Conflicts represent overlapping allocations within the global timetable. The evaluation metric counts one conflict *for every distinct overlapping event*.

- **Classroom Conflict**: Occurs when two or more distinct courses are allocated to the same `Classroom_ID` during the same `Time_Slot_ID`.
- **Lecturer Conflict**: Occurs when two or more distinct courses taught by the same `Lecturer_ID` are allocated to the same `Time_Slot_ID`, regardless of the assigned classroom.
- **Student-Group Conflict**: Occurs when two or more distinct courses attended by the same `Student_Group` are allocated to the same `Time_Slot_ID`.

## 2. Physical Violation Definitions (Hard Constraints)
Violations occur when a course is allocated to a physical space that does not meet its synthetic requirements.

- **Capacity Violation**: The `Number_of_Students` enrolled in the course exceeds the `Capacity` of the assigned classroom.
- **Room-Type Violation**: The `Required_Room_Type` (e.g., "Lecture Hall", "Laboratory") does not match the `Room_Type` of the assigned classroom.
- **Facility Violation**: The classroom's `Facilities` array does not contain all items listed in the course's `Required_Facilities` array.
- **Availability Violation**: The course is assigned to a `Time_Slot_ID` that is not listed in the classroom's physical `Availability` schedule.

## 3. Allocation Definitions
- **Unallocated Course**: A course that is not assigned a complete valid tuple of `(Classroom_ID, Time_Slot_ID)`.
- **Allocated Course**: A course that receives an assignment, regardless of whether that assignment generates conflicts or physical violations.

## 4. Utilization Definition (Soft Objective)
Utilization measures the spatial efficiency of the scheduled timetable. It is calculated identically for both algorithms:

`Overall Utilization = (Total Student Slot-Hours Assigned / Total Capacity Slot-Hours Available) * 100`

**Formula specifics**:
1. For every allocated course, the number of students is multiplied by the course duration (in slots). This calculates `Total Student Slot-Hours`.
2. For every allocated course, the assigned classroom's total capacity is multiplied by the course duration (in slots). This calculates `Total Capacity Slot-Hours`.
3. The sum of (1) is divided by the sum of (2) to yield the percentage.

This formula ensures that duration is appropriately weighted (a 2-slot class uses twice the capacity time as a 1-slot class) and prevents multi-slot courses from skewing the utilization average compared to single-slot courses.
