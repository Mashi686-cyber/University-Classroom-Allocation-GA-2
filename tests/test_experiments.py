import pytest
import os
import csv
from src.experiments.parameter_experiments import run_experiment_suite, BASE_PARAMS

def test_experiment_runner_config_generation(tmp_path):
    # Change current working directory to the temp path for testing output
    # But wait, load_dataset relies on fixed path. We'll mock the dataset loading or just use a small mock.
    pass # I'll use a better mocking approach

def test_experiment_runner(mocker, tmp_path):
    # Mock load_dataset so we don't need real files and it runs instantly
    courses = [{"Course_ID": "C1", "Duration": "1", "Number_of_Students": "10", "Required_Room_Type": "Lecture Hall", "Required_Facilities": "[]", "Lecturer_ID": "L1", "Student_Group": "SG1", "Course_Name": "C1"}]
    classrooms = [{"Classroom_ID": "R1", "Capacity": "20", "Room_Type": "Lecture Hall", "Facilities": "[]", "Availability": '["TS1"]'}]
    timeslots = [{"Time_Slot_ID": "TS1", "Day": "Mon", "Start_Time": "08:00", "End_Time": "09:00"}]
    
    mocker.patch("src.experiments.parameter_experiments.load_dataset", return_value=(courses, classrooms, timeslots))
    
    # We also mock os.makedirs to not pollute root, and write to tmp_path
    def mock_makedirs(name, exist_ok=False):
        pass
    mocker.patch("os.makedirs", side_effect=mock_makedirs)
    
    # We need to mock the csv open so it writes to tmp_path
    original_open = open
    def mock_open(file, *args, **kwargs):
        if "results/experiments" in file:
            file = os.path.join(tmp_path, os.path.basename(file))
        return original_open(file, *args, **kwargs)
    mocker.patch("builtins.open", side_effect=mock_open)

    import src.genetic_algorithm.genetic_algorithm
    spy = mocker.spy(src.genetic_algorithm.genetic_algorithm.GeneticAlgorithm, "__init__")
    
    # Run a tiny suite
    results = run_experiment_suite("test_exp", "population_size", [10, 20], dataset="small")
    
    # Verify configurations generated correctly and only intended parameter changes
    assert spy.call_count == 2
    args_call_1 = spy.call_args_list[0][1]['config']
    args_call_2 = spy.call_args_list[1][1]['config']
    
    assert args_call_1['population_size'] == 10
    assert args_call_2['population_size'] == 20
    
    assert args_call_1['generations'] == BASE_PARAMS['generations']
    assert args_call_2['generations'] == BASE_PARAMS['generations']
    
    assert args_call_1['random_seed'] == 42
    assert args_call_2['random_seed'] == 42

    # Verify results are saved correctly
    out_file = os.path.join(tmp_path, "test_exp_results.csv")
    assert os.path.exists(out_file)
    with original_open(out_file, 'r') as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2
        assert reader[0]['parameter'] == 'population_size'
        assert reader[0]['value'] == '10'

    # Verify all configurations executed
    assert len(results) == 2
