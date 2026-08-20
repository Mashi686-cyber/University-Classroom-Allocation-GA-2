# Final Demo Checklist

Use this checklist during your live presentation or recording to guarantee a flawless end-to-end demonstration of the UniClass-GA optimization suite.

- [x] **Start application**: Run `./start.sh` or `start.bat` and verify both backend and frontend launch cleanly on ports 8000 and 3000 respectively.
- [x] **Dashboard**: Open `http://localhost:3000`. Show the high-level KPI cards and dynamic performance comparison chart.
- [x] **Dataset validation**: Navigate to Datasets, select the Small dataset, and trigger the Validation check to confirm zero warnings or errors. Show the tabbed data grids.
- [x] **GA configuration**: Navigate to Allocation. Select Genetic Algorithm and input the experimental configuration (Pop: 50, Gen: 50, Crossover: 0.8, Mutation: 0.1, Elite: 2, Seed: 42).
- [x] **Run GA**: Execute the allocation. Show the loading states and wait for the "completed" status.
- [x] **Results**: Open the Results history table. Click into the latest run to observe the detailed metrics breakdown (Conflicts, Utilization, Execution Time).
- [x] **Timetable**: Navigate into the Timetable view. Point out that courses accurately span multiple hours (if `Duration > 1`) and align correctly with classroom assignments and lecturer IDs.
- [x] **Baseline comparison**: Navigate to the Comparison page. Demonstrate the visual charting comparing the Baseline vs Genetic Algorithm across metrics.
- [x] **Parameter experiments**: Navigate to Experiments. Show how the LineCharts dynamically present the Phase 5 empirical data for Population Size, Generations, etc.
- [x] **Research findings**: Navigate to Research Findings. Read out the conclusions for RQ1-RQ4, confirming they match the academic evidence matrix.
- [x] **Mobile view**: Shrink the browser window to mobile width (e.g. 390px) to demonstrate responsive cards, collapsing sidebars, and safe horizontal scroll boundaries.
- [x] **No console errors**: Open Chrome DevTools and verify a clean console output with 0 runtime or hydration errors.
- [x] **Build passes**: Mention or show that the production Next.js build passes cleanly.
- [x] **Tests pass**: Mention or show that the Python algorithmic `pytest` suite passes 100%.
- [x] **Windows launcher reviewed**: Mention the cross-platform nature of `start.py`, validating it is native Python/Node and requires no WSL dependency.
