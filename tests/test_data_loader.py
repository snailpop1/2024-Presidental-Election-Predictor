import csv

from data_loader import read_polling_data, read_state_list, read_states_info


def test_read_states_info(tmp_path):
    file = tmp_path / "states.csv"
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "electoral_votes"])
        writer.writeheader()
        writer.writerow({"name": "Alpha", "electoral_votes": 3})
    states = read_states_info(str(file))
    assert "Alpha" in states
    assert states["Alpha"].electoral_votes == 3


def test_read_state_list(tmp_path):
    file = tmp_path / "states.txt"
    file.write_text("Alpha\nBeta\n")
    result = read_state_list(str(file))
    assert result == ["Alpha", "Beta"]


def test_read_polling_data(tmp_path):
    file = tmp_path / "polls.csv"
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["state_name", "harris_support", "trump_support", "weight", "moe"]
        )
        writer.writeheader()
        writer.writerow(
            {
                "state_name": "Alpha",
                "harris_support": 52.0,
                "trump_support": 48.0,
                "weight": 3,
                "moe": 4.0,
            }
        )
    polling = read_polling_data(str(file))
    assert polling[0]["state_name"] == "Alpha"
    assert polling[0]["weight"] == 3
