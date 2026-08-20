import json

class ConstraintChecker:
    def __init__(self, courses, classrooms, timeslots):
        self.courses = {c["Course_ID"]: c for c in courses}
        self.classrooms = {r["Classroom_ID"]: r for r in classrooms}
        self.timeslots = {ts["Time_Slot_ID"]: ts for ts in timeslots}

    def evaluate(self, allocations):
        """
        Evaluate hard constraints for a given set of allocations.
        Allocations is a list of dicts.
        """
        violations = {
            "classroom_conflicts": 0,
            "lecturer_conflicts": 0,
            "student_group_conflicts": 0,
            "capacity_violations": 0,
            "facility_violations": 0,
            "room_type_violations": 0,
            "availability_violations": 0,
            "unallocated_courses": 0
        }
        
        # Unallocated courses
        allocated_course_ids = set([a["Course_ID"] for a in allocations])
        violations["unallocated_courses"] = len(self.courses) - len(allocated_course_ids)

        # Track usage for conflict detection
        # Dictionary keys: (Classroom_ID, Time_Slot_ID) -> list of courses
        classroom_usage = {}
        # Dictionary keys: (Lecturer_ID, Time_Slot_ID) -> list of courses
        lecturer_usage = {}
        # Dictionary keys: (Student_Group, Time_Slot_ID) -> list of courses
        student_group_usage = {}

        for alloc in allocations:
            c_id = alloc["Course_ID"]
            r_id = alloc["Classroom_ID"]
            
            # Timeslots can be a list if comma-separated
            ts_list = [ts.strip() for ts in alloc["Time_Slot_ID"].split(",")] if alloc["Time_Slot_ID"] else []
            
            # Course requirements
            course = self.courses.get(c_id, {})
            num_students = int(course.get("Number_of_Students", alloc.get("Number_of_Students", 0)))
            req_room_type = course.get("Required_Room_Type", alloc.get("Required_Room_Type", ""))
            req_fac = json.loads(course.get("Required_Facilities", "[]"))
            lecturer_id = course.get("Lecturer_ID", alloc.get("Lecturer_ID", ""))
            student_group = course.get("Student_Group", alloc.get("Student_Group", ""))

            # Classroom constraints
            classroom = self.classrooms.get(r_id, {})
            capacity = int(classroom.get("Capacity", 0))
            room_type = classroom.get("Room_Type", "")
            facilities = json.loads(classroom.get("Facilities", "[]"))
            availability = json.loads(classroom.get("Availability", "[]"))

            # 4. Capacity Violation
            if num_students > capacity:
                violations["capacity_violations"] += 1

            # 5. Facility Mismatch
            if not all(f in facilities for f in req_fac):
                violations["facility_violations"] += 1

            # 6. Room Type Mismatch
            if req_room_type != room_type:
                violations["room_type_violations"] += 1

            # Populate usage tracking and check availability per timeslot
            for ts in ts_list:
                # 7. Availability Violation
                if ts not in availability:
                    violations["availability_violations"] += 1

                # Tracking for conflicts
                classroom_usage.setdefault((r_id, ts), []).append(c_id)
                lecturer_usage.setdefault((lecturer_id, ts), []).append(c_id)
                student_group_usage.setdefault((student_group, ts), []).append(c_id)

        # Count overlaps
        for courses_in_slot in classroom_usage.values():
            if len(courses_in_slot) > 1:
                # E.g. 3 courses in same slot means 2 conflict overlaps
                violations["classroom_conflicts"] += (len(courses_in_slot) - 1)

        for courses_in_slot in lecturer_usage.values():
            if len(courses_in_slot) > 1:
                violations["lecturer_conflicts"] += (len(courses_in_slot) - 1)

        for courses_in_slot in student_group_usage.values():
            if len(courses_in_slot) > 1:
                violations["student_group_conflicts"] += (len(courses_in_slot) - 1)

        return violations
