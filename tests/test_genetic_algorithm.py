import pytest
from src.genetic_algorithm.chromosome import Chromosome
from src.genetic_algorithm.config import GA_PARAMS, PENALTY_WEIGHTS
from src.genetic_algorithm.selection import tournament_selection
from src.genetic_algorithm.crossover import uniform_crossover
from src.genetic_algorithm.mutation import mutate
from src.genetic_algorithm.fitness import FitnessEvaluator
from src.genetic_algorithm.genetic_algorithm import GeneticAlgorithm

def get_dummy_data():
    courses = [
        {"Course_ID": "C1", "Course_Name": "C1", "Number_of_Students": "50", "Required_Room_Type": "Lecture Hall", "Required_Facilities": '["Projector"]', "Lecturer_ID": "L1", "Student_Group": "SG1", "Duration": "1"},
        {"Course_ID": "C2", "Course_Name": "C2", "Number_of_Students": "30", "Required_Room_Type": "Laboratory", "Required_Facilities": '["Computers"]', "Lecturer_ID": "L2", "Student_Group": "SG2", "Duration": "2"}
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
    # pre-calculated valid windows
    ts_windows = {
        1: ["TS1", "TS2", "TS3"],
        2: ["TS1,TS2", "TS2,TS3"]
    }
    return courses, classrooms, timeslots, ts_windows

def test_chromosome_creation_and_duration_handling():
    courses, classrooms, timeslots, ts_windows = get_dummy_data()
    chrom = Chromosome()
    chrom.randomize(courses, classrooms, ts_windows)
    
    # C2 has duration 2, should have a valid window
    c2_gene = chrom.genes["C2"]
    assert c2_gene[1] in ts_windows[2]
    
    # C1 has duration 1
    c1_gene = chrom.genes["C1"]
    assert c1_gene[1] in ts_windows[1]
    


def test_selection():
    c1 = Chromosome()
    c1.fitness = -100
    c2 = Chromosome()
    c2.fitness = -50
    c3 = Chromosome()
    c3.fitness = -200
    pop = [c1, c2, c3]
    
    best = tournament_selection(pop, k=3)
    assert best == c2
    
def test_crossover():
    c1 = Chromosome({"C1": ("R1", "TS1")})
    c2 = Chromosome({"C1": ("R2", "TS2")})
    child1, child2 = uniform_crossover(c1, c2)
    assert child1.genes["C1"][0] in ["R1", "R2"]
    
def test_mutation():
    courses, classrooms, timeslots, ts_windows = get_dummy_data()
    c1 = Chromosome({"C1": ("R1", "TS1"), "C2": ("R1", "TS1,TS2")})
    
    # mutate with 1.0 rate forces mutation
    mutate(c1, 1.0, courses, classrooms, ts_windows)
    assert "C1" in c1.genes
    
def test_reproducibility():
    courses, classrooms, timeslots, ts_windows = get_dummy_data()
    
    # Run 1
    ga1 = GeneticAlgorithm(courses, classrooms, timeslots, config={"population_size": 10, "generations": 2, "crossover_rate": 0.8, "mutation_rate": 0.1, "elitism": 2, "random_seed": 42})
    r1 = ga1.run()
    
    # Run 2
    ga2 = GeneticAlgorithm(courses, classrooms, timeslots, config={"population_size": 10, "generations": 2, "crossover_rate": 0.8, "mutation_rate": 0.1, "elitism": 2, "random_seed": 42})
    r2 = ga2.run()
    
    assert r1["final_fitness"] == r2["final_fitness"]
