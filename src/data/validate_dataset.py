import os
import csv
import json

SIZES = ["small", "medium", "large"]

def load_csv(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found.")
        return []
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))

def validate_dataset(size):
    print(f"--- Validating {size.upper()} dataset ---")
    base_dir = f"data/generated/{size}"
    
    courses = load_csv(f"{base_dir}/courses.csv")
    classrooms = load_csv(f"{base_dir}/classrooms.csv")
    lecturers = load_csv(f"{base_dir}/lecturers.csv")
    student_groups = load_csv(f"{base_dir}/student_groups.csv")
    timeslots = load_csv(f"{base_dir}/timeslots.csv")
    
    warnings = 0
    errors = 0
    
    # 1. Unique IDs
    c_ids = [c["Course_ID"] for c in courses]
    r_ids = [r["Classroom_ID"] for r in classrooms]
    l_ids = [l["Lecturer_ID"] for l in lecturers]
    sg_ids = [sg["Student_Group_ID"] for sg in student_groups]
    ts_ids = [ts["Time_Slot_ID"] for ts in timeslots]
    
    if len(c_ids) != len(set(c_ids)): print("ERROR: Duplicate Course IDs"); errors += 1
    if len(r_ids) != len(set(r_ids)): print("ERROR: Duplicate Classroom IDs"); errors += 1
    if len(l_ids) != len(set(l_ids)): print("ERROR: Duplicate Lecturer IDs"); errors += 1
    if len(sg_ids) != len(set(sg_ids)): print("ERROR: Duplicate Student Group IDs"); errors += 1
    if len(ts_ids) != len(set(ts_ids)): print("ERROR: Duplicate Timeslot IDs"); errors += 1
    
    # 2. Valid foreign-key relationships
    l_id_set = set(l_ids)
    sg_id_set = set(sg_ids)
    
    for c in courses:
        if c["Lecturer_ID"] not in l_id_set:
            print(f"ERROR: Course {c['Course_ID']} has invalid Lecturer_ID {c['Lecturer_ID']}")
            errors += 1
        if c["Student_Group"] not in sg_id_set:
            print(f"ERROR: Course {c['Course_ID']} has invalid Student_Group {c['Student_Group']}")
            errors += 1
            
        # 3. No missing required values
        for key, val in c.items():
            if not val or val.strip() == "":
                print(f"ERROR: Course {c['Course_ID']} missing value for {key}")
                errors += 1
                
        # Valid duration
        if int(c["Duration"]) <= 0:
            print(f"ERROR: Course {c['Course_ID']} has invalid Duration")
            errors += 1
            
        # Match student count (warning if they don't match, though our generator makes them match)
        for sg in student_groups:
            if sg["Student_Group_ID"] == c["Student_Group"]:
                if sg["Student_Count"] != c["Number_of_Students"]:
                    print(f"WARNING: Course {c['Course_ID']} students count ({c['Number_of_Students']}) != group count ({sg['Student_Count']})")
                    warnings += 1
    
    # Valid capacities & room types
    room_types_present = set()
    for r in classrooms:
        if int(r["Capacity"]) <= 0:
            print(f"ERROR: Classroom {r['Classroom_ID']} has invalid Capacity")
            errors += 1
        room_types_present.add(r["Room_Type"])
        
    for c in courses:
        if c["Required_Room_Type"] not in room_types_present:
            print(f"WARNING: Course {c['Course_ID']} requires room type '{c['Required_Room_Type']}' but no such rooms exist.")
            warnings += 1
            
    print(f"Validation complete: {errors} Errors, {warnings} Warnings.")
    return errors, warnings

def main():
    total_errors = 0
    total_warnings = 0
    for size in SIZES:
        e, w = validate_dataset(size)
        total_errors += e
        total_warnings += w
        
    if total_errors == 0:
        print("\nSUCCESS: All datasets passed validation.")
    else:
        print(f"\nFAILED: Validation found {total_errors} errors.")

if __name__ == "__main__":
    main()
