import pytest

from models import State


def test_add_poll_weight_validation():
    state = State("Test", 10)
    with pytest.raises(ValueError):
        state.add_poll(50.0, 50.0, 0, 3.0)
    state.add_poll(51.0, 49.0, 5, 4.0)
    assert len(state.polls) == 1


def test_calculate_weighted_support():
    state = State("Test", 10)
    state.add_poll(55.0, 45.0, 2, 3.0)
    state.add_poll(50.0, 50.0, 1, 4.0)
    state.calculate_weighted_support()
    assert round(state.harris_support, 2) == 53.33
    assert round(state.trump_support, 2) == 46.67
    assert state.std_dev >= 1.0
