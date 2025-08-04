"""Simulation logic for the election model."""

from __future__ import annotations

import argparse
import csv
import os
import random
from typing import Dict, Optional

from data_loader import read_polling_data, read_state_list, read_states_info
from models import State


def simulate_election(
    states: Dict[str, State],
    simulations: int = 1000,
    poll_uncertainty: float = 1.0,
    turnout_scenario: Optional[Dict[str, float]] = None,
) -> Dict[str, int]:
    """Run election simulations.

    Args:
        states: Mapping of state name to State objects.
        simulations: Number of Monte Carlo runs.
        poll_uncertainty: Multiplier applied to each state's standard deviation.
        turnout_scenario: Optional mapping of state name to margin shift in favor of
            Harris (negative values benefit Trump).
    Returns:
        Dictionary with counts for Harris wins, Trump wins and ties.
    """
    turnout_scenario = turnout_scenario or {}
    harris_wins = 0
    trump_wins = 0
    ties = 0

    for _ in range(simulations):
        harris_evs = 0
        trump_evs = 0
        for state in states.values():
            adjustment = turnout_scenario.get(state.name, 0.0)
            harris_margin = state.harris_support - state.trump_support + adjustment
            std_dev = state.std_dev * poll_uncertainty
            harris_margin_result = random.gauss(harris_margin, std_dev)
            if harris_margin_result > 0:
                harris_evs += state.electoral_votes
            else:
                trump_evs += state.electoral_votes

        if harris_evs >= 270:
            harris_wins += 1
        elif trump_evs >= 270:
            trump_wins += 1
        else:
            ties += 1

    return {"harris_wins": harris_wins, "trump_wins": trump_wins, "ties": ties}


def load_default_states() -> Dict[str, State]:
    """Load state and polling information using default data files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    states_info_path = os.path.join(data_dir, "states_info.csv")
    safe_states_harris_path = os.path.join(data_dir, "safe_states_harris.txt")
    safe_states_trump_path = os.path.join(data_dir, "safe_states_trump.txt")
    competitive_states_path = os.path.join(data_dir, "competitive_states.txt")
    polling_data_path = os.path.join(data_dir, "polling_data.csv")

    states = read_states_info(states_info_path)
    safe_states_harris = read_state_list(safe_states_harris_path)
    safe_states_trump = read_state_list(safe_states_trump_path)

    for state_name in safe_states_harris:
        if state_name in states:
            state = states[state_name]
            state.harris_support = 60.0
            state.trump_support = 35.0
            state.std_dev = 2.0

    for state_name in safe_states_trump:
        if state_name in states:
            state = states[state_name]
            state.harris_support = 35.0
            state.trump_support = 60.0
            state.std_dev = 2.0

    competitive_states = read_state_list(competitive_states_path)
    polling_data = read_polling_data(polling_data_path)

    for poll in polling_data:
        state_name = poll["state_name"]
        if state_name in states:
            state = states[state_name]
            state.add_poll(
                harris_support=poll["harris_support"],
                trump_support=poll["trump_support"],
                weight=poll["weight"],
                moe=poll["moe"],
            )

    for state_name in competitive_states:
        if state_name in states:
            states[state_name].calculate_weighted_support()

    return states


def read_turnout_adjustments(filename: str) -> Dict[str, float]:
    """Read turnout adjustments from a CSV file."""
    adjustments: Dict[str, float] = {}
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            adjustments[row["state_name"]] = float(row["margin_shift"])
    return adjustments


def main() -> None:
    parser = argparse.ArgumentParser(description="Run election simulations")
    parser.add_argument("--simulations", type=int, default=1000, help="Number of simulations to run")
    parser.add_argument(
        "--poll-uncertainty",
        type=float,
        default=1.0,
        help="Multiplier for poll standard deviations",
    )
    parser.add_argument(
        "--turnout-file",
        type=str,
        default=None,
        help="CSV file with state_name and margin_shift for turnout scenarios",
    )
    args = parser.parse_args()

    states = load_default_states()
    turnout = read_turnout_adjustments(args.turnout_file) if args.turnout_file else None
    results = simulate_election(
        states,
        simulations=args.simulations,
        poll_uncertainty=args.poll_uncertainty,
        turnout_scenario=turnout,
    )

    print(f"\nOut of {args.simulations} simulations:")
    print(f"Kamala Harris wins: {results['harris_wins']} times")
    print(f"Donald Trump wins: {results['trump_wins']} times")
    print(f"Ties or no majority: {results['ties']} times")


if __name__ == "__main__":
    main()
