import os
import csv
import json
import time

class BaselineAllocator:
    def __init__(self, courses, classrooms, timeslots):
        self.courses = sorted(courses, key=lambda c: c["Course_ID"])
        self.classrooms = sorted(classrooms, key=lambda r: r["Classroom_ID"])
        self.timeslots = sorted(timeslots, key=lambda ts: ts["Time_Slot_ID"])
        
        # Determine consecutive timeslots pre-calculation
        self.timeslot_windows = {}
        for duration in [1, 2]:
            windows = []
            for i in range(len(self.timeslots)):
                window = [self.timeslots[i]]
                valid = True
                for j in range(1, duration):
                    if i + j >= len(self.timeslots):
                        valid = False
                        break
                    prev_ts = self.timeslots[i + j - 1]
                    curr_ts = self.timeslots[i + j]
                    
                    if prev_ts["Day"] != curr_ts["Day"] or prev_ts["End_Time"] != curr_ts["Start_Time"]:
                        valid = False
                        break
                    window.append(curr_ts)
                if valid:
                    windows.append([ts["Time_Slot_ID"] for ts in window])
            self.timeslot_windows[duration] = windows

    def allocate(self):
        allocations = []
        classroom_schedule = {r["Classroom_ID"]: set() for r in self.classrooms}
        
        for course in self.courses:
            c_id = course["Course_ID"]
            num_students = int(course["Number_of_Students"])
            req_room_type = course["Required_Room_Type"]
            req_fac = json.loads(course["Required_Facilities"])
            duration = int(course["Duration"])
            
            allocated = False
            for classroom in self.classrooms:
                if allocated: break
                
                r_id = classroom["Classroom_ID"]
                capacity = int(classroom["Capacity"])
                room_type = classroom["Room_Type"]
                facilities = json.loads(classroom["Facilities"])
                availability = set(json.loads(classroom["Availability"]))
                
                # Check hard physical constraints
                if capacity < num_students:
                    continue
                if room_type != req_room_type:
                    continue
                if not all(f in facilities for f in req_fac):
                    continue
                    
                # Find available timeslot window
                for window in self.timeslot_windows.get(duration, []):
                    # Check if all slots in window are available for this room
                    if all(ts in availability and ts not in classroom_schedule[r_id] for ts in window):
                        # Found a slot!
                        for ts in window:
                            classroom_schedule[r_id].add(ts)
                            
                        allocations.append({
                            "Course_ID": c_id,
                            "Course_Name": course["Course_Name"],
                            "Student_Group": course["Student_Group"],
                            "Lecturer_ID": course["Lecturer_ID"],
                            "Classroom_ID": r_id,
                            "Time_Slot_ID": ",".join(window),
                            "Number_of_Students": num_students,
                            "Classroom_Capacity": capacity,
                            "Required_Room_Type": req_room_type,
                            "Required_Facilities": json.dumps(req_fac),
                            "Duration": duration
                        })
                        allocated = True
                        break
                        
        return allocations

def run_baseline_for_dataset(size):
    base_dir = f"data/generated/{size}"
    
    def load_csv(name):
        with open(f"{base_dir}/{name}", 'r') as f:
            return list(csv.DictReader(f))
            
    start_time = time.time()
    
    courses = load_csv("courses.csv")
    classrooms = load_csv("classrooms.csv")
    timeslots = load_csv("timeslots.csv")
    
    allocator = BaselineAllocator(courses, classrooms, timeslots)
    allocations = allocator.allocate()
    
    exec_time = time.time() - start_time
    
    # Save allocations
    if allocations:
        keys = allocations[0].keys()
        out_file = f"results/baseline/{size}_baseline.csv"
        with open(out_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(allocations)
            
    return allocations, courses, classrooms, timeslots, exec_time

if __name__ == "__main__":
    from src.evaluation.constraint_checker import ConstraintChecker
    from src.evaluation.metrics import MetricsCalculator
    import json
    
    for size in ["small", "medium", "large"]:
        print(f"Running baseline for {size} dataset...")
        allocations, courses, classrooms, timeslots, exec_time = run_baseline_for_dataset(size)
        
        checker = ConstraintChecker(courses, classrooms, timeslots)
        violations = checker.evaluate(allocations)
        
        metrics_calc = MetricsCalculator(classrooms)
        overall_util, _ = metrics_calc.calculate_utilization(allocations)
        
        summary = {
            "total_courses": len(courses),
            "allocated_courses": len(allocations),
            "unallocated_courses": violations["unallocated_courses"],
            "classroom_conflicts": violations["classroom_conflicts"],
            "lecturer_conflicts": violations["lecturer_conflicts"],
            "student_group_conflicts": violations["student_group_conflicts"],
            "capacity_violations": violations["capacity_violations"],
            "facility_violations": violations["facility_violations"],
            "room_type_violations": violations["room_type_violations"],
            "availability_violations": violations["availability_violations"],
            "utilization": overall_util,
            "execution_time_seconds": exec_time
        }
        
        with open(f"results/baseline/{size}_summary.json", 'w') as f:
            json.dump(summary, f, indent=4)
            
        print(f"Summary for {size}:")
        print(json.dumps(summary, indent=2))
        print("-" * 40)
