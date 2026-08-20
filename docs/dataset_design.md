# Dataset Design and Methodology

## 1. Why Synthetic Data is Required
University classroom allocation involves numerous strict constraints (capacities, facilities, lecturer availability, student group scheduling, specific room types). Obtaining public datasets that include all these nuanced, interdependent variables is extremely difficult due to privacy and proprietary concerns. Therefore, we generate a highly structured synthetic dataset that accurately models a realistic university environment to evaluate our Genetic Algorithm.

## 2. Dataset Generation Methodology
The dataset is generated using a deterministic Python script (`src/data/generate_synthetic_data.py`). 
It produces entities systematically to maintain proper referential integrity:
1. **Timeslots**: Available time windows for scheduling.
2. **Student Groups**: Cohorts with specific student counts.
3. **Lecturers**: Available teaching staff.
4. **Classrooms**: Physical rooms with realistic capacities (30-150), room types (Lecture Hall, Laboratory, Seminar Room), and combinations of facilities (Projector, Computers, Smart Board, Sound System).
5. **Courses**: Scheduled classes that map to a specific Student Group and Lecturer. Each course is assigned realistic requirements based on its type (e.g., Labs require Computers; large courses require large rooms).

The script uses standard library functions and a fixed random seed to ensure exact reproducibility across multiple runs.

## 3. Dataset Assumptions
- A student group takes multiple courses.
- A course has exactly one designated lecturer.
- Classrooms have fixed, unchanging capacities and facilities.
- Timeslots are predefined and standardized (e.g., 1-hour blocks).
- "Duration" indicates the number of consecutive or separate timeslots required by a course.

## 4. Attribute Definitions & Relationships
* **`courses.csv`**: `Course_ID`, `Course_Name`, `Student_Group` (FK), `Number_of_Students` (derived from FK), `Lecturer_ID` (FK), `Required_Room_Type`, `Required_Facilities`, `Duration`.
* **`classrooms.csv`**: `Classroom_ID`, `Capacity`, `Room_Type`, `Facilities`, `Availability`.
* **`lecturers.csv`**: `Lecturer_ID`, `Lecturer_Name`.
* **`student_groups.csv`**: `Student_Group_ID`, `Student_Count`.
* **`timeslots.csv`**: `Time_Slot_ID`, `Day`, `Start_Time`, `End_Time`.

## 5. Dataset Sizes
Three scaled datasets were generated to test performance and scalability:
- **Small**: 20 courses, 10 student groups, 12 lecturers, 10 classrooms, 20 timeslots.
- **Medium**: 50 courses, 10 student groups, 22 lecturers, 15 classrooms, 25 timeslots.
- **Large**: 100 courses, 10 student groups, 35 lecturers, 20 classrooms, 30 timeslots.

## 6. Random Seed
A fixed random seed (`42`) is used in the generator. This ensures that any researcher or reviewer running the generator will obtain the exact same records, conflicts, and edge cases, supporting reproducible benchmarking between the baseline algorithm and the Genetic Algorithm.

## 7. Validation Rules
The generated data passes strict referential integrity checks via `src/data/validate_dataset.py`:
- Unique IDs for all primary keys.
- All foreign keys correctly point to existing primary keys.
- No missing or null values in required fields.
- Room capacities and course durations are strictly positive integers.
- Required room types by courses exist in the pool of available classrooms.

## 8. Limitations
- Does not currently model travel time between buildings.
- Assumes a simplified block-based timeslot system rather than highly variable irregular durations.
- Does not include lecturer specific unavailability (e.g. sick days) outside of algorithmic scheduling constraints.
