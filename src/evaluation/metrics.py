class MetricsCalculator:
    def __init__(self, classrooms):
        self.classrooms = {r["Classroom_ID"]: r for r in classrooms}

    def calculate_utilization(self, allocations):
        """
        Calculates classroom utilization.
        Returns overall utilization percentage and a list of individual course utilizations.
        """
        individual_utils = []
        total_students_assigned = 0
        total_capacity_used = 0

        for alloc in allocations:
            num_students = int(alloc.get("Number_of_Students", 0))
            r_id = alloc["Classroom_ID"]
            classroom = self.classrooms.get(r_id, {})
            capacity = int(classroom.get("Capacity", 1)) # avoid div by zero
            
            # Duration in slots
            ts_list = [ts for ts in alloc["Time_Slot_ID"].split(",") if ts.strip()]
            duration = max(1, len(ts_list))
            
            util = (num_students / capacity) * 100
            individual_utils.append({
                "Course_ID": alloc["Course_ID"],
                "Utilization": util
            })
            
            total_students_assigned += (num_students * duration)
            total_capacity_used += (capacity * duration)

        overall_utilization = 0
        if total_capacity_used > 0:
            overall_utilization = (total_students_assigned / total_capacity_used) * 100

        return overall_utilization, individual_utils
