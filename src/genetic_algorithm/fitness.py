from src.evaluation.constraint_checker import ConstraintChecker
from src.evaluation.metrics import MetricsCalculator
from src.genetic_algorithm.config import PENALTY_WEIGHTS

class FitnessEvaluator:
    def __init__(self, courses, classrooms, timeslots):
        self.courses = courses
        self.checker = ConstraintChecker(courses, classrooms, timeslots)
        self.metrics = MetricsCalculator(classrooms)

    def evaluate(self, chromosome):
        """
        Calculates fitness based on penalty weights and utilization.
        """
        allocations = chromosome.to_allocations(self.courses)
        violations = self.checker.evaluate(allocations)
        overall_util, _ = self.metrics.calculate_utilization(allocations)
        
        fitness = 0.0
        
        # Apply penalties
        for key, weight in PENALTY_WEIGHTS.items():
            fitness -= (violations.get(key, 0) * weight)
            
        # Add soft objective (Utilization)
        # Utilization is 0 to 100. We add it to fitness to encourage better packed rooms.
        fitness += overall_util
        
        chromosome.fitness = fitness
        return fitness, violations, overall_util
