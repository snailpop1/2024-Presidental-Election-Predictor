# US Presidential Election Simulation (Harris vs. Trump)

## Project Overview

This project simulates the outcome of a hypothetical US presidential election between Kamala Harris and Donald Trump based on state classifications (safe/competitive) and polling data. It runs multiple simulations to estimate the probability of each candidate reaching the 270 electoral votes needed to win.

## Simulation Pipeline

The simulation is broken into three stages represented by separate classes in
`simulation_pipeline.py`:

1. **PollDataSource** – loads state and polling information. The default
   implementation, `CSVFilePollDataSource`, reads the CSV and text files in the
   `data/` directory.
2. **SimulationEngine** – performs the Monte Carlo simulations. The repository
   includes `MonteCarloSimulationEngine`, but new strategies can be added by
   subclassing `SimulationEngine`.
3. **ResultAnalyzer** – interprets raw simulation output. `BasicResultAnalyzer`
   counts wins for each candidate. Custom analysers can compute additional
   metrics.

`election_simulation.py` wires these pieces together to run the default
forecast.

## Data Files (`data/` directory)

* `competitive_states.txt`: A text file listing the names of states considered competitive, one state per line.
* `polling_data.csv`: A CSV file containing polling results. Expected columns: `state_name`, `harris_support`, `trump_support`, `weight` (poll importance/reliability, 1-10), `moe` (margin of error).
* `safe_states_harris.txt`: A text file listing states considered safely voting for Harris, one state per line.
* `safe_states_trump.txt`: A text file listing states considered safely voting for Trump, one state per line.
* `states_info.csv`: A CSV file containing state details. Expected columns: `name` (state name), `electoral_votes`.

## Files in Project

* `simulation_pipeline.py`: Core classes for data loading, simulation and
  result analysis.
* `election_simulation.py`: Small entry script that runs the default pipeline.
* `data/`: Directory containing all necessary data files.
* `README.md`: This file.

## How to Run

1.  Ensure you have Python installed.
2.  Make sure all data files are present in the `data/` subdirectory relative to the script.
3.  Run the script from your terminal:
    ```bash
    python election_simulation.py
    ```
4.  The script will output the simulation results, showing the number of times each candidate won out of the total simulations performed.

## Dependencies

The script uses standard Python libraries:
* `csv`
* `random`
* `os`
* `collections` (specifically `defaultdict`, though not explicitly used in the final version provided)

No external libraries need to be installed.

## Extending the Pipeline

The modular design allows new forecasting features. For example, to experiment
with a different simulation strategy:

```python
from simulation_pipeline import MonteCarloSimulationEngine, SimulationEngine

class AlwaysHarrisWins(SimulationEngine):
    def run(self, states, simulations):
        return [{"Harris": 538, "Trump": 0} for _ in range(simulations)]
```

More complete examples are provided in `examples/`.
