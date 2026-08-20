# Default GA parameters for initial experiment
GA_PARAMS = {
    "population_size": 50,
    "generations": 100,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "elitism": 2,
    "random_seed": 42
}

# Penalty weights for fitness function
PENALTY_WEIGHTS = {
    "unallocated_courses": 100000,
    "classroom_conflicts": 10000,
    "lecturer_conflicts": 10000,
    "student_group_conflicts": 10000,
    "capacity_violations": 10000,
    "facility_violations": 10000,
    "room_type_violations": 10000,
    "availability_violations": 10000
}
