"""Core components for the election forecasting pipeline.

This module defines abstract base classes and default implementations for
loading polling data, running simulations, and analyzing results.  The
interfaces make it easy to plug in alternative data sources or simulation
strategies.

Example of extending the simulation:

    class AlwaysTrumpWinsEngine(SimulationEngine):
        def run(self, states, simulations):
            return [{'Harris': 0, 'Trump': 538} for _ in range(simulations)]

    data = CSVFilePollDataSource('data').get_states()
    engine = AlwaysTrumpWinsEngine()
    results = engine.run(data, simulations=100)
    summary = BasicResultAnalyzer().summarize(results)
"""

from __future__ import annotations

import csv
import os
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class State:
    """Represents a state in the election simulation."""

    name: str
    electoral_votes: int
    polls: List[Dict[str, float]] = field(default_factory=list)
    harris_support: float = 50.0
    trump_support: float = 50.0
    std_dev: float = 4.0

    def add_poll(self, harris_support: float, trump_support: float, weight: int, moe: float) -> None:
        """Adds a poll to the state."""
        if weight < 1 or weight > 10:
            raise ValueError("Weight must be between 1 and 10")
        self.polls.append(
            {
                "harris": harris_support,
                "trump": trump_support,
                "weight": weight,
                "moe": moe,
            }
        )

    def calculate_weighted_support(self) -> None:
        """Calculates weighted support and standard deviation based on polls."""
        total_weight = sum(poll["weight"] for poll in self.polls)
        if total_weight == 0:
            self.harris_support = 50.0
            self.trump_support = 50.0
            self.std_dev = 2.0
            return

        harris_total = sum(poll["harris"] * poll["weight"] for poll in self.polls)
        trump_total = sum(poll["trump"] * poll["weight"] for poll in self.polls)
        self.harris_support = harris_total / total_weight
        self.trump_support = trump_total / total_weight

        weighted_moe = sum(poll["moe"] * poll["weight"] for poll in self.polls) / total_weight
        self.std_dev = max(weighted_moe / 1.96, 1.0)


class PollDataSource(ABC):
    """Interface for loading polling data."""

    @abstractmethod
    def get_states(self) -> Dict[str, State]:
        """Return a mapping of state name to :class:`State`."""


class CSVFilePollDataSource(PollDataSource):
    """Load polling data from CSV and text files in a directory."""

    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir

    def _read_states_info(self, filename: str) -> Dict[str, State]:
        states: Dict[str, State] = {}
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                states[row["name"]] = State(row["name"], int(row["electoral_votes"]))
        return states

    def _read_state_list(self, filename: str) -> List[str]:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    def _read_polling_data(self, filename: str) -> List[Dict[str, str]]:
        polling_data: List[Dict[str, str]] = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                polling_data.append(
                    {
                        "state_name": row["state_name"],
                        "harris_support": float(row["harris_support"]),
                        "trump_support": float(row["trump_support"]),
                        "weight": int(row["weight"]),
                        "moe": float(row["moe"]),
                    }
                )
        return polling_data

    def get_states(self) -> Dict[str, State]:
        states_info_path = os.path.join(self.data_dir, "states_info.csv")
        safe_states_harris_path = os.path.join(self.data_dir, "safe_states_harris.txt")
        safe_states_trump_path = os.path.join(self.data_dir, "safe_states_trump.txt")
        competitive_states_path = os.path.join(self.data_dir, "competitive_states.txt")
        polling_data_path = os.path.join(self.data_dir, "polling_data.csv")

        states = self._read_states_info(states_info_path)

        safe_states_harris = self._read_state_list(safe_states_harris_path)
        safe_states_trump = self._read_state_list(safe_states_trump_path)

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

        competitive_states = self._read_state_list(competitive_states_path)
        polling_data = self._read_polling_data(polling_data_path)

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


class SimulationEngine(ABC):
    """Interface for running election simulations."""

    @abstractmethod
    def run(self, states: Dict[str, State], simulations: int) -> List[Dict[str, int]]:
        """Run simulations and return a list of results per simulation."""


class MonteCarloSimulationEngine(SimulationEngine):
    """Default Monte Carlo simulation engine."""

    def run(self, states: Dict[str, State], simulations: int) -> List[Dict[str, int]]:
        results: List[Dict[str, int]] = []
        for _ in range(simulations):
            harris_evs = 0
            trump_evs = 0
            for state in states.values():
                margin = state.harris_support - state.trump_support
                outcome = random.gauss(margin, state.std_dev)
                if outcome > 0:
                    harris_evs += state.electoral_votes
                else:
                    trump_evs += state.electoral_votes
            results.append({"Harris": harris_evs, "Trump": trump_evs})
        return results


class ResultAnalyzer(ABC):
    """Interface for analyzing simulation results."""

    @abstractmethod
    def summarize(self, results: List[Dict[str, int]]) -> Dict[str, int]:
        """Return summary statistics from simulation results."""


class BasicResultAnalyzer(ResultAnalyzer):
    """Count wins for each candidate."""

    def summarize(self, results: List[Dict[str, int]]) -> Dict[str, int]:
        summary = {"Harris": 0, "Trump": 0, "Ties": 0}
        for result in results:
            if result["Harris"] >= 270:
                summary["Harris"] += 1
            elif result["Trump"] >= 270:
                summary["Trump"] += 1
            else:
                summary["Ties"] += 1
        return summary
