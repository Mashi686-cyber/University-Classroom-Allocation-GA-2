# Dataset Analysis and Project Planning

## 1. Dataset Inventory
The project directory contains two main data sources:
1. **OULAD (Open University Learning Analytics Dataset)**: A collection of CSV files (`courses.csv`, `assessments.csv`, `vle.csv`, `studentInfo.csv`, `studentAssessment.csv`, `studentRegistration.csv`, `studentVle.csv`).
2. **Timetabling Optimisation Solution**: A single Excel file (`Timetabling Optimisation Solution.xlsx`).

## 2. Dataset Structure
- **Timetabling Optimisation Solution.xlsx**: Contains 22 records with 6 columns (`Module code`, `Module title`, `Day`, `Start time`, `End time`, `Rating`).
- **OULAD (e.g., studentInfo.csv)**: Contains 32,593 records with 12 columns covering demographic and academic performance data.
- **OULAD (e.g., courses.csv)**: Contains 22 records with 3 columns (`code_module`, `code_presentation`, `module_presentation_length`).

## 3. Column Analysis
### Timetabling Optimisation Solution
- `Module code` (str): Course identifier (e.g., BS101).
- `Module title` (str): Name of the course.
- `Day` (str): Day of the week.
- `Start time`, `End time` (str): Time schedule.
- `Rating` (float): Unknown rating metric.

### OULAD
- Focuses on student interactions (`id_student`, `gender`, `highest_education`, `final_result`), online module presentations, and VLE (Virtual Learning Environment) clicks.

## 4. Data Quality Analysis
- **Timetabling Optimisation Solution.xlsx**: 
  - Contains 17 missing values across schedule columns out of 22 records.
  - Contains 9 duplicate records.
- **OULAD**:
  - `studentInfo.csv`: 1,111 missing values in `imd_band`.
  - `vle.csv`: High number of missing values (5,243) in `week_from` and `week_to`.

## 5. Useful Attributes
- From the Excel file: `Module code`, `Module title`.
- From OULAD: Potentially module codes, but mostly irrelevant.

## 6. Unnecessary Attributes
- Almost all columns in OULAD (gender, disability, IMD band, VLE interactions, assessment dates) are unnecessary for physical classroom allocation.
- The `Rating` column in the timetabling Excel file is not applicable.

## 7. Missing Information
To solve the University Classroom Allocation Optimization problem using a Genetic Algorithm, the following critical data points are entirely missing:
- **Classrooms**: Capacity, room types, facilities (projectors, labs), availability.
- **Lecturers**: IDs, names, mapping to courses, availability.
- **Student Groups**: Group IDs, exact student counts, mapping to courses.
- **Courses (Constraints)**: Required room types, required facilities, required duration.
- **Timeslots**: Formal definition of all available scheduling slots.

## 8. Relationship Between Datasets
There is no meaningful relationship between the `Timetabling Optimisation Solution.xlsx` and the OULAD CSV files. They come from different domains (a sample timetable vs. online distance learning analytics).

## 9. Suitability for University Classroom Allocation
**Neither dataset is suitable for this research project.**
- OULAD is designed for predicting student performance in an online/distance learning environment and lacks physical infrastructure data.
- The Excel file is a tiny, incomplete schedule output rather than a set of inputs for an allocation problem. It lacks constraints like capacities, facilities, and lecturers.

## 10. Recommended Final Dataset Design
Since real-world university timetabling datasets with all constraints are difficult to obtain publicly, we must generate a high-quality, realistic synthetic dataset. 

### Proposed Schema

**COURSES**
- `Course_ID` (str): Unique identifier.
- `Course_Name` (str): Name of the course.
- `Student_Group` (str): Foreign key to STUDENT_GROUPS.
- `Number_of_Students` (int): Number of students enrolled.
- `Lecturer_ID` (str): Foreign key to LECTURERS.
- `Required_Room_Type` (str): e.g., "Lecture Hall", "Laboratory".
- `Required_Facilities` (list): e.g., ["Projector", "Computers"].
- `Duration` (int): Number of timeslots required.

**CLASSROOMS**
- `Classroom_ID` (str): Unique identifier.
- `Capacity` (int): Maximum student capacity.
- `Room_Type` (str): e.g., "Lecture Hall", "Laboratory".
- `Facilities` (list): Available equipment.
- `Availability` (list/dict): Available timeslots for the classroom.

**LECTURERS**
- `Lecturer_ID` (str): Unique identifier.
- `Lecturer_Name` (str): Name of the lecturer.

**STUDENT_GROUPS**
- `Student_Group_ID` (str): Unique identifier.
- `Student_Count` (int): Total students in the group.

**TIMESLOTS**
- `Time_Slot_ID` (str): Unique identifier (e.g., TS_MON_01).
- `Day` (str): Day of the week.
- `Start_Time` (str): Time string.
- `End_Time` (str): Time string.

### Validation Rules
- Capacity >= Number_of_Students for assigned rooms.
- Required_Room_Type must match Room_Type.
- Required_Facilities must be a subset of Facilities.
- Lecturer_ID, Student_Group, and Course_ID must exist in their respective tables.
- No duplicate records in primary tables.
- No missing values in primary constraints.

---

## Recommended Repository Structure
```
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── generated/
├── src/
│   ├── data/
│   ├── baseline/
│   ├── genetic_algorithm/
│   ├── evaluation/
│   └── visualization/
├── tests/
├── experiments/
├── results/
├── docs/
│   └── dataset_analysis.md
├── requirements.txt
└── README.md
```

## Next Phase Recommendation
We should proceed to **Phase 2: Dataset Design and Preprocessing**, where we will:
1. Establish the repository structure.
2. Write a Python script (`src/data/generate_synthetic_data.py`) to generate realistic synthetic data matching the proposed schema.
3. Apply validation logic to ensure the dataset has no missing values, valid relationships, and enough complexity to test hard constraints (conflicts) and soft constraints (utilization).
