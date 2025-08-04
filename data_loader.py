"""Functions for loading election data."""

from __future__ import annotations

import csv
from typing import Dict, List

from models import State


def read_states_info(filename: str) -> Dict[str, State]:
    """Read states information and return mapping of name to State."""
    states: Dict[str, State] = {}
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            electoral_votes = int(row["electoral_votes"])
            states[name] = State(name, electoral_votes)
    return states


def read_state_list(filename: str) -> List[str]:
    """Read a list of state names from a text file."""
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def read_polling_data(filename: str) -> List[Dict[str, float]]:
    """Read polling data and return a list of poll records."""
    polling_data: List[Dict[str, float]] = []
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
