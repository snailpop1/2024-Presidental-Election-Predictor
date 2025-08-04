"""Models for election simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


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
        """Calculates weighted support and standard deviation from polls."""
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
        self.std_dev = weighted_moe / 1.96
        if self.std_dev < 1.0:
            self.std_dev = 1.0
