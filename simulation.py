import csv
import os
from collections import defaultdict

import argparse
import numpy as np


class State:
    """
    Represents a state in the election simulation.
    """

    def __init__(self, name, electoral_votes):
        self.name = name
        self.electoral_votes = electoral_votes
        self.polls = []
        self.harris_support = 50.0
        self.trump_support = 50.0
        self.std_dev = 4.0  

    def add_poll(self, harris_support, trump_support, weight, moe):
        """
        Adds a poll to the state.
        """
        if weight < 1 or weight > 10:
            raise ValueError("Weight must be between 1 and 10")
        self.polls.append({
            'harris': harris_support,
            'trump': trump_support,
            'weight': weight,
            'moe': moe
        })

    def calculate_weighted_support(self):
        """
        Calculates the weighted support for Harris and Trump based on polls.
        Also calculates the standard deviation based on the weighted MOE.
        """
        total_weight = sum(poll['weight'] for poll in self.polls)
        if total_weight == 0:
            self.harris_support = 50.0
            self.trump_support = 50.0
            self.std_dev = 2.0  
            return

        harris_total = sum(poll['harris'] * poll['weight'] for poll in self.polls)
        trump_total = sum(poll['trump'] * poll['weight'] for poll in self.polls)
        self.harris_support = harris_total / total_weight
        self.trump_support = trump_total / total_weight

        weighted_moe = sum(poll['moe'] * poll['weight'] for poll in self.polls) / total_weight

        self.std_dev = weighted_moe / 1.96

        if self.std_dev < 1.0:
            self.std_dev = 1.0  


def read_states_info(filename):
    """
    Reads states information from a CSV file and returns a dictionary of State objects.
    """
    states = {}
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            electoral_votes = int(row['electoral_votes'])
            states[name] = State(name, electoral_votes)
    return states


def read_state_list(filename):
    """
    Reads a list of states from a text file.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        states = [line.strip() for line in file if line.strip()]
    return states


def read_polling_data(filename):
    """
    Reads polling data from a CSV file and returns a list of dictionaries.
    """
    polling_data = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            polling_data.append({
                'state_name': row['state_name'],
                'harris_support': float(row['harris_support']),
                'trump_support': float(row['trump_support']),
                'weight': int(row['weight']),
                'moe': float(row['moe'])
            })
    return polling_data


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(script_dir, 'data')

    states_info_path = os.path.join(data_dir, 'states_info.csv')
    safe_states_harris_path = os.path.join(data_dir, 'safe_states_harris.txt')
    safe_states_trump_path = os.path.join(data_dir, 'safe_states_trump.txt')
    competitive_states_path = os.path.join(data_dir, 'competitive_states.txt')
    polling_data_path = os.path.join(data_dir, 'polling_data.csv')

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
        state_name = poll['state_name']
        if state_name in states:
            state = states[state_name]
            state.add_poll(
                harris_support=poll['harris_support'],
                trump_support=poll['trump_support'],
                weight=poll['weight'],
                moe=poll['moe']
            )

    for state_name in competitive_states:
        if state_name in states:
            state = states[state_name]
            state.calculate_weighted_support()

    parser = argparse.ArgumentParser(description="Simulate election outcomes")
    parser.add_argument("--simulations", type=int, default=1000,
                        help="Number of simulation runs")
    args = parser.parse_args()

    simulations = args.simulations

    state_list = list(states.values())
    margins = np.array(
        [s.harris_support - s.trump_support for s in state_list],
        dtype=np.float32,
    )
    std_devs = np.array([s.std_dev for s in state_list], dtype=np.float32)
    evs = np.array([s.electoral_votes for s in state_list], dtype=np.int16)
    total_ev = np.int32(evs.sum())

    harris_evs = np.zeros(simulations, dtype=np.int16)
    rng = np.random.default_rng()
    for margin, sd, ev in zip(margins, std_devs, evs):
        results = rng.normal(margin, sd, simulations).astype(np.float32)
        harris_evs += (results > 0).astype(np.int16) * ev

    trump_evs = total_ev - harris_evs

    harris_wins = np.count_nonzero(harris_evs >= 270)
    trump_wins = np.count_nonzero(trump_evs >= 270)
    ties = simulations - harris_wins - trump_wins

    print(f"\nOut of {simulations} simulations:")
    print(f"Kamala Harris wins: {harris_wins} times")
    print(f"Donald Trump wins: {trump_wins} times")
    print(f"Ties or no majority: {ties} times")


if __name__ == '__main__':
    main()
