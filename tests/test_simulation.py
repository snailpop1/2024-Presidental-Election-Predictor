from models import State
from simulation import simulate_election


def test_simulation_deterministic_with_poll_uncertainty_zero():
    state = State("Test", 300)
    state.harris_support = 55.0
    state.trump_support = 45.0
    state.std_dev = 5.0
    states = {"Test": state}
    results = simulate_election(states, simulations=1, poll_uncertainty=0)
    assert results["harris_wins"] == 1
    assert results["trump_wins"] == 0


def test_turnout_scenario_changes_result():
    state = State("Test", 300)
    state.harris_support = 45.0
    state.trump_support = 55.0
    state.std_dev = 0.0
    states = {"Test": state}
    no_shift = simulate_election(states, simulations=1)
    assert no_shift["trump_wins"] == 1
    shift = simulate_election(states, simulations=1, turnout_scenario={"Test": 15.0})
    assert shift["harris_wins"] == 1
