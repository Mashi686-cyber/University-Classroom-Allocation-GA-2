import random
import json

def mutate(chromosome, mutation_rate, courses, classrooms, timeslot_windows):
    """
    Mutates genes based on mutation_rate.
    A mutation replaces the current assignment with a new random feasible assignment.
    """
    for c in courses:
        if random.random() < mutation_rate:
            duration = int(c["Duration"])
            valid_windows = timeslot_windows.get(duration, [])
            
            # Lightweight Repair/Validity Strategy
            req_fac = json.loads(c["Required_Facilities"])
            valid_classrooms = [
                r for r in classrooms
                if int(r["Capacity"]) >= int(c["Number_of_Students"])
                and r["Room_Type"] == c["Required_Room_Type"]
                and all(f in json.loads(r["Facilities"]) for f in req_fac)
            ]
            
            if not valid_windows or not valid_classrooms:
                chromosome.genes[c["Course_ID"]] = (None, None)
                continue
                
            r_id = random.choice(valid_classrooms)["Classroom_ID"]
            t_window = random.choice(valid_windows)
            
            chromosome.genes[c["Course_ID"]] = (r_id, t_window)
