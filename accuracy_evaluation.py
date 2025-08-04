import csv
import os
import random

from election_simulation import (
    read_states_info,
    read_state_list,
    read_polling_data,
)


def build_states(data_dir):
    states_info_path = os.path.join(data_dir, 'states_info.csv')
    states = read_states_info(states_info_path)

    safe_harris_path = os.path.join(data_dir, 'safe_states_harris.txt')
    safe_trump_path = os.path.join(data_dir, 'safe_states_trump.txt')
    competitive_path = os.path.join(data_dir, 'competitive_states.txt')
    polling_data_path = os.path.join(data_dir, 'polling_data.csv')

    safe_harris = read_state_list(safe_harris_path)
    safe_trump = read_state_list(safe_trump_path)
    competitive_states = read_state_list(competitive_path)
    polling_data = read_polling_data(polling_data_path)

    for state_name in safe_harris:
        if state_name in states:
            state = states[state_name]
            state.harris_support = 60.0
            state.trump_support = 35.0
            state.std_dev = 2.0

    for state_name in safe_trump:
        if state_name in states:
            state = states[state_name]
            state.harris_support = 35.0
            state.trump_support = 60.0
            state.std_dev = 2.0

    for poll in polling_data:
        state_name = poll['state_name']
        if state_name in states:
            state = states[state_name]
            state.add_poll(
                harris_support=poll['harris_support'],
                trump_support=poll['trump_support'],
                weight=poll['weight'],
                moe=poll['moe'],
            )

    for state_name in competitive_states:
        if state_name in states:
            states[state_name].calculate_weighted_support()

    return states


def simulate_state_winners(states, simulations=1000, seed=42):
    random.seed(seed)
    win_counts = {name: {'Harris': 0, 'Trump': 0} for name in states}
    for _ in range(simulations):
        for state in states.values():
            margin = state.harris_support - state.trump_support
            result = random.gauss(margin, state.std_dev)
            if result > 0:
                win_counts[state.name]['Harris'] += 1
            else:
                win_counts[state.name]['Trump'] += 1
    predictions = {}
    for name, counts in win_counts.items():
        winner = 'Democrat' if counts['Harris'] >= counts['Trump'] else 'Republican'
        predictions[name] = winner
    return predictions


def load_historical_results(path):
    results = {}
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results[row['state_name']] = row['winner']
    return results


def evaluate_accuracy(predicted, actual):
    total = 0
    correct = 0
    for state, actual_winner in actual.items():
        if state in predicted:
            total += 1
            if predicted[state] == actual_winner:
                correct += 1
    accuracy = (correct / total * 100) if total > 0 else 0
    return accuracy, correct, total


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    historical_path = os.path.join(data_dir, 'historical_results.csv')

    states = build_states(data_dir)
    predictions = simulate_state_winners(states)
    historical_results = load_historical_results(historical_path)
    accuracy, correct, total = evaluate_accuracy(predictions, historical_results)

    print(f"Predicted correctly for {correct} out of {total} states.")
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == '__main__':
    main()
