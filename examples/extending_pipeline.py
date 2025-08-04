"""Demonstrates how to plug custom components into the simulation pipeline."""

import os
import sys

# Allow running this file directly by adding the project root to ``sys.path``.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulation_pipeline import (
    BasicResultAnalyzer,
    PollDataSource,
    SimulationEngine,
    State,
)

class StaticPollDataSource(PollDataSource):
    """Provide a single fictional state with fixed support numbers."""

    def get_states(self):  # type: ignore[override]
        demo_state = State("Nowhere", 10)
        demo_state.harris_support = 55.0
        demo_state.trump_support = 45.0
        demo_state.std_dev = 3.0
        return {demo_state.name: demo_state}


class AlwaysTrumpWinsEngine(SimulationEngine):
    """A toy simulation that awards all EVs to Trump regardless of polls."""

    def run(self, states, simulations):  # type: ignore[override]
        total_evs = sum(state.electoral_votes for state in states.values())
        return [{"Harris": 0, "Trump": total_evs} for _ in range(simulations)]


if __name__ == "__main__":
    source = StaticPollDataSource()
    states = source.get_states()
    engine = AlwaysTrumpWinsEngine()
    analyzer = BasicResultAnalyzer()

    results = engine.run(states, simulations=5)
    print(analyzer.summarize(results))
