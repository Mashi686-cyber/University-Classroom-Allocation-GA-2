import json
from src.evaluation.constraint_checker import ConstraintChecker
from src.evaluation.metrics import MetricsCalculator
from src.baseline.baseline_allocator import BaselineAllocator

def get_dummy_data():
    courses = [
        {"Course_ID": "C1", "Course_Name": "Course 1", "Number_of_Students": "50", "Required_Room_Type": "Lecture Hall", "Required_Facilities": '["Projector"]', "Lecturer_ID": "L1", "Student_Group": "SG1", "Duration": "1"},
        {"Course_ID": "C2", "Course_Name": "Course 2", "Number_of_Students": "30", "Required_Room_Type": "Laboratory", "Required_Facilities": '["Computers"]', "Lecturer_ID": "L2", "Student_Group": "SG2", "Duration": "2"}
    ]
    classrooms = [
        {"Classroom_ID": "R1", "Capacity": "60", "Room_Type": "Lecture Hall", "Facilities": '["Projector", "Whiteboard"]', "Availability": '["TS1", "TS2", "TS3"]'},
        {"Classroom_ID": "R2", "Capacity": "40", "Room_Type": "Laboratory", "Facilities": '["Computers"]', "Availability": '["TS1", "TS2", "TS3"]'}
    ]
    timeslots = [
        {"Time_Slot_ID": "TS1", "Day": "Monday", "Start_Time": "08:00", "End_Time": "09:00"},
        {"Time_Slot_ID": "TS2", "Day": "Monday", "Start_Time": "09:00", "End_Time": "10:00"},
        {"Time_Slot_ID": "TS3", "Day": "Monday", "Start_Time": "10:00", "End_Time": "11:00"}
    ]
    return courses, classrooms, timeslots

def test_capacity_facility_roomtype_checking():
    courses, classrooms, timeslots = get_dummy_data()
    # Modify dummy data to force a violation if we bypass the allocator (testing checker)
    allocations = [
        {"Course_ID": "C1", "Classroom_ID": "R2", "Time_Slot_ID": "TS1", "Number_of_Students": 50, "Required_Room_Type": "Lecture Hall"}
    ]
    checker = ConstraintChecker(courses, classrooms, timeslots)
    v = checker.evaluate(allocations)
    
    # C1 in R2:
    # R2 capacity is 40, students 50 -> capacity violation
    # R2 is Laboratory, C1 needs Lecture Hall -> room type violation
    # R2 has Computers, C1 needs Projector -> facility violation
    assert v["capacity_violations"] == 1
    assert v["room_type_violations"] == 1
    assert v["facility_violations"] == 1

def test_conflicts_detection():
    courses, classrooms, timeslots = get_dummy_data()
    allocations = [
        {"Course_ID": "C1", "Classroom_ID": "R1", "Time_Slot_ID": "TS1"},
        {"Course_ID": "C2", "Classroom_ID": "R1", "Time_Slot_ID": "TS1"}
    ]
    checker = ConstraintChecker(courses, classrooms, timeslots)
    v = checker.evaluate(allocations)
    assert v["classroom_conflicts"] == 1
    assert v["lecturer_conflicts"] == 0
    assert v["student_group_conflicts"] == 0

def test_lecturer_student_conflicts():
    courses, classrooms, timeslots = get_dummy_data()
    # Force same lecturer and student group
    courses[1]["Lecturer_ID"] = "L1"
    courses[1]["Student_Group"] = "SG1"
    
    allocations = [
        {"Course_ID": "C1", "Classroom_ID": "R1", "Time_Slot_ID": "TS1"},
        {"Course_ID": "C2", "Classroom_ID": "R2", "Time_Slot_ID": "TS1"}
    ]
    checker = ConstraintChecker(courses, classrooms, timeslots)
    v = checker.evaluate(allocations)
    assert v["lecturer_conflicts"] == 1
    assert v["student_group_conflicts"] == 1

def test_duration_handling():
    courses, classrooms, timeslots = get_dummy_data()
    allocator = BaselineAllocator(courses, classrooms, timeslots)
    allocs = allocator.allocate()
    
    c2_alloc = next(a for a in allocs if a["Course_ID"] == "C2")
    # C2 has duration 2, should occupy two slots
    slots = c2_alloc["Time_Slot_ID"].split(",")
    assert len(slots) == 2
    assert slots[0] == "TS1"
    assert slots[1] == "TS2"

def test_utilization_calculation():
    courses, classrooms, timeslots = get_dummy_data()
    allocations = [
        {"Course_ID": "C1", "Classroom_ID": "R1", "Time_Slot_ID": "TS1", "Number_of_Students": 30},
        {"Course_ID": "C2", "Classroom_ID": "R2", "Time_Slot_ID": "TS2,TS3", "Number_of_Students": 40}
    ]
    metrics = MetricsCalculator(classrooms)
    util, ind = metrics.calculate_utilization(allocations)
    # C1: 30 / 60 = 50% (duration 1) -> students=30, cap=60
    # C2: 40 / 40 = 100% (duration 2) -> students=80, cap=80
    # Total students = 110. Total cap = 140. Util = 110 / 140 * 100 = 78.57%
    assert abs(util - 78.57) < 0.1

def test_unallocated_course_detection():
    courses, classrooms, timeslots = get_dummy_data()
    # Allocator gets C1 and C2, but we pass only C1 to checker
    allocations = [
        {"Course_ID": "C1", "Classroom_ID": "R1", "Time_Slot_ID": "TS1"}
    ]
    checker = ConstraintChecker(courses, classrooms, timeslots)
    v = checker.evaluate(allocations)
    assert v["unallocated_courses"] == 1
