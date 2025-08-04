"""Entry point for running the election simulation pipeline."""

import os

from simulation_pipeline import (
    BasicResultAnalyzer,
    CSVFilePollDataSource,
    MonteCarloSimulationEngine,
)


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    data_source = CSVFilePollDataSource(data_dir)
    states = data_source.get_states()

    engine = MonteCarloSimulationEngine()
    results = engine.run(states, simulations=1000)

    analyzer = BasicResultAnalyzer()
    summary = analyzer.summarize(results)

    print(f"\nOut of {len(results)} simulations:")
    print(f"Kamala Harris wins: {summary['Harris']} times")
    print(f"Donald Trump wins: {summary['Trump']} times")
    print(f"Ties or no majority: {summary['Ties']} times")


if __name__ == "__main__":
    main()
