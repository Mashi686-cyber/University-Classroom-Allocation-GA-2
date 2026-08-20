import random
import json

class Chromosome:
    """
    Represents a full timetable allocation for all courses.
    The genes are stored as a dictionary mapping Course_ID to a tuple:
    (Classroom_ID, Time_Slot_Window)
    
    Time_Slot_Window is a comma-separated string of consecutive timeslot IDs 
    satisfying the course's duration.
    """
    def __init__(self, genes=None):
        self.genes = genes if genes else {}
        self.fitness = None

    def randomize(self, courses, classrooms, timeslot_windows):
        """
        Initializes the chromosome with random feasible assignments from the available pool.
        timeslot_windows is a dict: duration -> list of valid window strings (e.g., "TS001,TS002")
        """
        self.genes = {}
        for c in courses:
            duration = int(c["Duration"])
            valid_windows = timeslot_windows.get(duration, [])
            
            # Lightweight Repair/Validity Strategy: 
            # Only choose from classrooms that physically fit the course.
            req_fac = json.loads(c["Required_Facilities"])
            valid_classrooms = [
                r for r in classrooms
                if int(r["Capacity"]) >= int(c["Number_of_Students"])
                and r["Room_Type"] == c["Required_Room_Type"]
                and all(f in json.loads(r["Facilities"]) for f in req_fac)
            ]
            
            if not valid_windows or not valid_classrooms:
                self.genes[c["Course_ID"]] = (None, None)
                continue
                
            r_id = random.choice(valid_classrooms)["Classroom_ID"]
            t_window = random.choice(valid_windows)
            
            self.genes[c["Course_ID"]] = (r_id, t_window)

    def to_allocations(self, courses):
        """
        Converts the internal genes mapping into the allocation dict format 
        required by the constraint checker.
        """
        allocations = []
        for c in courses:
            c_id = c["Course_ID"]
            if c_id not in self.genes or self.genes[c_id][0] is None:
                continue # Unallocated
                
            r_id, t_window = self.genes[c_id]
            alloc = {
                "Course_ID": c_id,
                "Course_Name": c["Course_Name"],
                "Student_Group": c["Student_Group"],
                "Lecturer_ID": c["Lecturer_ID"],
                "Classroom_ID": r_id,
                "Time_Slot_ID": t_window,
                "Number_of_Students": int(c["Number_of_Students"]),
                "Required_Room_Type": c["Required_Room_Type"],
                "Required_Facilities": c["Required_Facilities"],
                "Duration": int(c["Duration"])
            }
            allocations.append(alloc)
        return allocations
