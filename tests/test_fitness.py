import pytest
from src.genetic_algorithm.chromosome import Chromosome
from src.genetic_algorithm.fitness import FitnessEvaluator
from src.genetic_algorithm.config import PENALTY_WEIGHTS

def get_base_data():
    courses = [
        {"Course_ID": "C1", "Course_Name": "C1", "Number_of_Students": "30", "Required_Room_Type": "Lecture Hall", "Required_Facilities": '[]', "Lecturer_ID": "L1", "Student_Group": "SG1", "Duration": "1"},
        {"Course_ID": "C2", "Course_Name": "C2", "Number_of_Students": "30", "Required_Room_Type": "Lecture Hall", "Required_Facilities": '[]', "Lecturer_ID": "L2", "Student_Group": "SG2", "Duration": "1"}
    ]
    classrooms = [
        {"Classroom_ID": "R1", "Capacity": "40", "Room_Type": "Lecture Hall", "Facilities": '["Projector"]', "Availability": '["TS1", "TS2"]'},
        {"Classroom_ID": "R2", "Capacity": "20", "Room_Type": "Laboratory", "Facilities": '[]', "Availability": '["TS1", "TS2"]'}
    ]
    timeslots = [
        {"Time_Slot_ID": "TS1", "Day": "Mon", "Start_Time": "08:00", "End_Time": "09:00"},
        {"Time_Slot_ID": "TS2", "Day": "Mon", "Start_Time": "09:00", "End_Time": "10:00"}
    ]
    return courses, classrooms, timeslots

def test_case_a_valid_allocation():
    courses, classrooms, timeslots = get_base_data()
    chrom = Chromosome({"C1": ("R1", "TS1"), "C2": ("R1", "TS2")})
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["capacity_violations"] == 0
    assert violations["classroom_conflicts"] == 0
    assert fitness > 0 # only utilization reward

def test_case_b_capacity_violation():
    courses, classrooms, timeslots = get_base_data()
    chrom = Chromosome({"C1": ("R2", "TS1")}) # R2 capacity 20, C1 needs 30
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["capacity_violations"] == 1
    assert fitness <= -PENALTY_WEIGHTS["capacity_violations"]

def test_case_c_room_type_violation():
    courses, classrooms, timeslots = get_base_data()
    chrom = Chromosome({"C1": ("R2", "TS1")}) # R2 is Lab, C1 needs Lecture Hall
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["room_type_violations"] == 1

def test_case_d_facility_violation():
    courses, classrooms, timeslots = get_base_data()
    courses[0]["Required_Facilities"] = '["Computers"]'
    chrom = Chromosome({"C1": ("R1", "TS1")}) # R1 doesn't have Computers
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["facility_violations"] == 1

def test_case_e_lecturer_conflict():
    courses, classrooms, timeslots = get_base_data()
    courses[1]["Lecturer_ID"] = "L1" # Same lecturer
    chrom = Chromosome({"C1": ("R1", "TS1"), "C2": ("R2", "TS1")})
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["lecturer_conflicts"] == 1

def test_case_f_student_group_conflict():
    courses, classrooms, timeslots = get_base_data()
    courses[1]["Student_Group"] = "SG1" # Same group
    chrom = Chromosome({"C1": ("R1", "TS1"), "C2": ("R2", "TS1")})
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["student_group_conflicts"] == 1

def test_case_g_unallocated_course():
    courses, classrooms, timeslots = get_base_data()
    chrom = Chromosome({"C1": ("R1", "TS1"), "C2": (None, None)})
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    fitness, violations, util = evaluator.evaluate(chrom)
    assert violations["unallocated_courses"] == 1
    assert fitness <= -PENALTY_WEIGHTS["unallocated_courses"] + 100

def test_case_h_utilization_priority():
    courses, classrooms, timeslots = get_base_data()
    # C1 has 30 students.
    # Put C1 in R1 (capacity 40) -> Util 75%
    chrom1 = Chromosome({"C1": ("R1", "TS1")})
    
    # Put C1 in R3 (capacity 30) -> Util 100%
    classrooms.append({"Classroom_ID": "R3", "Capacity": "30", "Room_Type": "Lecture Hall", "Facilities": '[]', "Availability": '["TS1"]'})
    chrom2 = Chromosome({"C1": ("R3", "TS1")})
    
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    f1, _, _ = evaluator.evaluate(chrom1)
    f2, _, _ = evaluator.evaluate(chrom2)
    
    # Both are valid (no penalties), so f2 should be greater due to better util
    assert f2 > f1

def test_case_i_hard_constraint_dominates_utilization():
    courses, classrooms, timeslots = get_base_data()
    
    # Chromosome 1: Valid allocation, but terrible utilization (0% effectively, or very low)
    # C1 (30 students) in R1 (capacity 40) -> 75% util
    # C2 (30 students) in R1 (capacity 40) TS2 -> 75% util
    chrom_valid = Chromosome({"C1": ("R1", "TS1"), "C2": ("R1", "TS2")})
    
    # Chromosome 2: 1 Lecturer Conflict, but 100% utilization
    courses[1]["Lecturer_ID"] = "L1" # induce conflict
    classrooms.append({"Classroom_ID": "R3", "Capacity": "30", "Room_Type": "Lecture Hall", "Facilities": '[]', "Availability": '["TS1"]'})
    chrom_invalid = Chromosome({"C1": ("R3", "TS1"), "C2": ("R3", "TS1")}) # conflict! Util 100%
    
    evaluator = FitnessEvaluator(courses, classrooms, timeslots)
    f_valid, v_valid, u_valid = evaluator.evaluate(chrom_valid)
    f_invalid, v_invalid, u_invalid = evaluator.evaluate(chrom_invalid)
    
    assert v_valid["lecturer_conflicts"] == 0
    assert v_invalid["lecturer_conflicts"] > 0
    assert u_invalid > u_valid
    
    # Even though invalid has higher util, the valid one MUST have higher fitness
    assert f_valid > f_invalid
