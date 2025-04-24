# US Presidential Election Simulation (Harris vs. Trump)

## Project Overview

This project simulates the outcome of a hypothetical US presidential election between Kamala Harris and Donald Trump based on state classifications (safe/competitive) and polling data. It runs multiple simulations to estimate the probability of each candidate reaching the 270 electoral votes needed to win.

## Simulation Logic (`election_simulation.py`)

The simulation works as follows:

1.  **Load State Data:** Reads basic state information, including names and electoral votes, from `data/states_info.csv`.
2.  **Classify States:**
    * Reads lists of states considered "safe" for Harris (`data/safe_states_harris.txt`) and Trump (`data/safe_states_trump.txt`). Assigns fixed support margins (e.g., 60/35) and a standard deviation to these states.
    * Reads a list of "competitive" states from `data/competitive_states.txt`.
3.  **Process Polling Data:**
    * Reads polling data for states from `data/polling_data.csv`, which includes Harris support, Trump support, poll weight, and margin of error (MOE).
    * For competitive states, calculates the weighted average support for each candidate based on the available polls.
    * Calculates a standard deviation for each competitive state based on the weighted average margin of error from its polls (Std Dev ≈ MOE / 1.96). If no polls are available or the calculated standard deviation is too low, default values are used.
4.  **Run Simulations:**
    * Performs a set number of simulations (e.g., 1000).
    * In each simulation:
        * For every state, it simulates the election outcome by drawing a random result from a normal (Gaussian) distribution. The distribution is centered around the calculated or assigned support margin (Harris % - Trump %) for that state, using the state's calculated or assigned standard deviation.
        * If the simulated margin is positive, Harris wins the state's electoral votes; otherwise, Trump wins them.
        * The total electoral votes for Harris and Trump are tallied for the simulation.
5.  **Aggregate Results:** Counts the number of simulations where Harris wins (≥ 270 EVs), Trump wins (≥ 270 EVs), or there is a tie/no majority.
6.  **Output:** Prints the final probabilities based on the simulation outcomes.

## Data Files (`data/` directory)

* `competitive_states.txt`: A text file listing the names of states considered competitive, one state per line.
* `polling_data.csv`: A CSV file containing polling results. Expected columns: `state_name`, `harris_support`, `trump_support`, `weight` (poll importance/reliability, 1-10), `moe` (margin of error).
* `safe_states_harris.txt`: A text file listing states considered safely voting for Harris, one state per line.
* `safe_states_trump.txt`: A text file listing states considered safely voting for Trump, one state per line.
* `states_info.csv`: A CSV file containing state details. Expected columns: `name` (state name), `electoral_votes`.

## Files in Project

* `election_simulation.py`: The main Python script that runs the election simulation.
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
