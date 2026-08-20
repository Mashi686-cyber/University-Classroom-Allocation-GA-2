import os
import csv
import random
import json

# Set fixed random seed for reproducibility
random.seed(42)

# Constants
ROOM_TYPES = ["Lecture Hall", "Laboratory", "Seminar Room"]
FACILITIES = ["Projector", "Computers", "Whiteboard", "Smart Board", "Sound System"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_TIMES = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]

# Configuration for different sizes
CONFIG = {
    "small": {
        "num_courses": 20,
        "num_student_groups": 10,
        "num_lecturers": 12,
        "num_classrooms": 10,
        "num_timeslots": 20
    },
    "medium": {
        "num_courses": 50,
        "num_student_groups": 10,
        "num_lecturers": 22,
        "num_classrooms": 15,
        "num_timeslots": 25
    },
    "large": {
        "num_courses": 100,
        "num_student_groups": 10,
        "num_lecturers": 35,
        "num_classrooms": 20,
        "num_timeslots": 30
    }
}

def generate_student_groups(num_groups):
    groups = []
    for i in range(1, num_groups + 1):
        # Realistic sizes for groups: e.g., 20 to 120
        count = random.choice([20, 30, 40, 50, 60, 80, 100, 120])
        groups.append({
            "Student_Group_ID": f"SG{i:02d}",
            "Student_Count": count
        })
    return groups

def generate_lecturers(num_lecturers):
    lecturers = []
    for i in range(1, num_lecturers + 1):
        lecturers.append({
            "Lecturer_ID": f"L{i:03d}",
            "Lecturer_Name": f"Lecturer {i}"
        })
    return lecturers

def generate_classrooms(num_classrooms, timeslot_ids):
    classrooms = []
    capacities = [30, 40, 60, 80, 120, 150]
    
    for i in range(1, num_classrooms + 1):
        room_type = random.choice(ROOM_TYPES)
        # Labs usually have specific facilities
        if room_type == "Laboratory":
            cap = random.choice([30, 40, 60])
            fac = ["Computers", "Projector", "Whiteboard"]
        elif room_type == "Seminar Room":
            cap = random.choice([30, 40])
            fac = random.sample(["Projector", "Whiteboard", "Smart Board"], k=random.randint(1, 2))
        else: # Lecture Hall
            cap = random.choice([60, 80, 120, 150])
            fac = random.sample(["Projector", "Whiteboard", "Sound System"], k=random.randint(1, 3))
            
        classrooms.append({
            "Classroom_ID": f"R{i:03d}",
            "Capacity": cap,
            "Room_Type": room_type,
            "Facilities": json.dumps(fac),
            "Availability": json.dumps(timeslot_ids)  # initially available all the time
        })
    return classrooms

def generate_timeslots(num_timeslots):
    timeslots = []
    count = 0
    # Generate timeslots systematically
    for day in DAYS:
        for st in START_TIMES:
            if count >= num_timeslots:
                break
            
            # Simple 1-hour duration for definition
            h, m = map(int, st.split(":"))
            end_h = h + 1
            et = f"{end_h:02d}:{m:02d}"
            
            count += 1
            timeslots.append({
                "Time_Slot_ID": f"TS{count:03d}",
                "Day": day,
                "Start_Time": st,
                "End_Time": et
            })
    return timeslots

def generate_courses(num_courses, student_groups, lecturers):
    courses = []
    for i in range(1, num_courses + 1):
        group = random.choice(student_groups)
        lecturer = random.choice(lecturers)
        
        # Course requires a room type
        room_type = random.choice(ROOM_TYPES)
        
        # Course required facilities
        if room_type == "Laboratory":
            req_fac = ["Computers"]
        elif room_type == "Seminar Room":
            req_fac = []
            if random.random() > 0.5: req_fac.append("Whiteboard")
        else:
            req_fac = []
            if random.random() > 0.3: req_fac.append("Projector")
        
        courses.append({
            "Course_ID": f"C{i:03d}",
            "Course_Name": f"Course {i}",
            "Student_Group": group["Student_Group_ID"],
            "Number_of_Students": group["Student_Count"],
            "Lecturer_ID": lecturer["Lecturer_ID"],
            "Required_Room_Type": room_type,
            "Required_Facilities": json.dumps(req_fac),
            "Duration": random.choice([1, 2]) # 1 or 2 slots
        })
    return courses

def save_csv(filename, data):
    if not data: return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def generate_and_save(size_name, config):
    base_dir = f"data/generated/{size_name}"
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. Generate Timeslots
    timeslots = generate_timeslots(config["num_timeslots"])
    timeslot_ids = [ts["Time_Slot_ID"] for ts in timeslots]
    
    # 2. Generate Student Groups
    student_groups = generate_student_groups(config["num_student_groups"])
    
    # 3. Generate Lecturers
    lecturers = generate_lecturers(config["num_lecturers"])
    
    # 4. Generate Classrooms
    classrooms = generate_classrooms(config["num_classrooms"], timeslot_ids)
    
    # 5. Generate Courses
    courses = generate_courses(config["num_courses"], student_groups, lecturers)
    
    # Save to CSV
    save_csv(f"{base_dir}/timeslots.csv", timeslots)
    save_csv(f"{base_dir}/student_groups.csv", student_groups)
    save_csv(f"{base_dir}/lecturers.csv", lecturers)
    save_csv(f"{base_dir}/classrooms.csv", classrooms)
    save_csv(f"{base_dir}/courses.csv", courses)
    
    print(f"[{size_name.upper()}] Dataset generated successfully in {base_dir}")

def main():
    for size_name, config in CONFIG.items():
        generate_and_save(size_name, config)

if __name__ == "__main__":
    main()
