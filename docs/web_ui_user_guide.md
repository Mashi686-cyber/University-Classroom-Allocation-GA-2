# UniClass GA - Web UI User Guide

The UniClass GA Web UI allows users to easily configure, run, and inspect University Classroom Allocation Optimization algorithms using a modern, interactive dashboard.

## 1. Starting the Application

To run the application, you need to start both the Python backend and the Next.js frontend.

### Start the Backend (FastAPI)
1. Open a terminal.
2. Navigate to the backend directory:
   ```bash
   cd web/backend
   ```
3. Run the development server (make sure you are using the project's virtual environment):
   ```bash
   ../../.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Start the Frontend (Next.js)
1. Open a second terminal.
2. Navigate to the frontend directory:
   ```bash
   cd web/frontend
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```
4. The web application is now available at: **http://localhost:3000**

## 2. Using the Dashboard

When you navigate to the URL, you will land on the **Dashboard**.
Here you can see a summary of the available datasets (Small, Medium, Large) including the number of courses, classrooms, and timeslots they contain.

## 3. Inspecting and Validating Datasets

1. Click on **Datasets** in the left sidebar.
2. Use the dropdown to select the dataset size you want to view.
3. The page displays the available courses and their constraints.
4. Click **Validate Dataset** to ensure the dataset has no structural errors or logical contradictions (e.g., missing classrooms for a specific required room type).

## 4. Running an Allocation

1. Click on **Allocation** in the left sidebar.
2. **Dataset:** Select the dataset you want to optimize (Small, Medium, Large).
3. **Algorithm:** Choose either **Baseline Heuristic** or **Genetic Algorithm**.
4. **Configuration (GA only):** If you selected the Genetic Algorithm, you can tune parameters such as Population Size, Generations, Crossover Rate, and Mutation Rate.
5. Click **Start Allocation Job**.
6. You will be redirected to the **Results** detail page where you can monitor the live progress of the algorithm.

## 5. Viewing Results and Timetable

Once the allocation is complete:
1. The Result Detail page displays an overview of conflicts, utilization, fitness score, and execution time.
2. A **Constraint Breakdown** shows exactly which constraints (capacity, room type, etc.) were violated, if any.
3. Click **View Timetable** to see the resulting schedule in a visual week-grid, mapped by Day and Time.

## 6. Comparing Algorithms

1. Click on **Comparison** in the left sidebar.
2. Select a dataset size.
3. The page displays side-by-side bar charts comparing the Baseline method against the Genetic Algorithm for Total Conflicts, Resource Utilization, Allocated Courses, and Execution Time.

## 7. Analyzing Experiments and Research

- **Experiments:** View interactive line charts mapping the effect of changing Population Size, Generations, Crossover Rate, and Mutation Rate on the final fitness and execution time.
- **Research:** Read the finalized academic findings regarding Conflict Reduction, Utilization, Parameter Effects, and Algorithm comparisons directly drawn from the Phase 6 and 7 evaluations.
