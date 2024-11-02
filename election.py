import random

class State:
    def __init__(self, name, electoral_votes):
        self.name = name
        self.electoral_votes = electoral_votes
        self.polls = []  
        self.harris_support = 50.0  
        self.trump_support = 50.0   
        self.std_dev = 4.0 

    def add_poll(self, harris_support, trump_support, weight, moe):
        if weight < 1 or weight > 10:
            raise ValueError("Weight must be between 1 and 10")
        self.polls.append({
            'harris': harris_support,
            'trump': trump_support,
            'weight': weight,
            'moe': moe
        })

    def calculate_weighted_support(self):
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
        self.std_dev = 4.0  

def main():
    states_info = [
        {'name': 'Alabama', 'electoral_votes': 9},
        {'name': 'Alaska', 'electoral_votes': 3},
        {'name': 'Arizona', 'electoral_votes': 11},
        {'name': 'Arkansas', 'electoral_votes': 6},
        {'name': 'California', 'electoral_votes': 54},
        {'name': 'Colorado', 'electoral_votes': 10},
        {'name': 'Connecticut', 'electoral_votes': 7},
        {'name': 'Delaware', 'electoral_votes': 3},
        {'name': 'District of Columbia', 'electoral_votes': 3},
        {'name': 'Florida', 'electoral_votes': 30},
        {'name': 'Georgia', 'electoral_votes': 16},
        {'name': 'Hawaii', 'electoral_votes': 4},
        {'name': 'Idaho', 'electoral_votes': 4},
        {'name': 'Illinois', 'electoral_votes': 19},
        {'name': 'Indiana', 'electoral_votes': 11},
        {'name': 'Iowa', 'electoral_votes': 6},
        {'name': 'Kansas', 'electoral_votes': 6},
        {'name': 'Kentucky', 'electoral_votes': 8},
        {'name': 'Louisiana', 'electoral_votes': 8},
        {'name': 'Maine At-Large', 'electoral_votes': 2},
        {'name': 'Maine CD1', 'electoral_votes': 1},
        {'name': 'Maine CD2', 'electoral_votes': 1},
        {'name': 'Maryland', 'electoral_votes': 10},
        {'name': 'Massachusetts', 'electoral_votes': 11},
        {'name': 'Michigan', 'electoral_votes': 15},
        {'name': 'Minnesota', 'electoral_votes': 10},
        {'name': 'Mississippi', 'electoral_votes': 6},
        {'name': 'Missouri', 'electoral_votes': 10},
        {'name': 'Montana', 'electoral_votes': 4},
        {'name': 'Nebraska At-Large', 'electoral_votes': 2},
        {'name': 'Nebraska CD1', 'electoral_votes': 1},
        {'name': 'Nebraska CD2', 'electoral_votes': 1},
        {'name': 'Nebraska CD3', 'electoral_votes': 1},
        {'name': 'Nevada', 'electoral_votes': 6},
        {'name': 'New Hampshire', 'electoral_votes': 4},
        {'name': 'New Jersey', 'electoral_votes': 14},
        {'name': 'New Mexico', 'electoral_votes': 5},
        {'name': 'New York', 'electoral_votes': 28},
        {'name': 'North Carolina', 'electoral_votes': 16},
        {'name': 'North Dakota', 'electoral_votes': 3},
        {'name': 'Ohio', 'electoral_votes': 17},
        {'name': 'Oklahoma', 'electoral_votes': 7},
        {'name': 'Oregon', 'electoral_votes': 8},
        {'name': 'Pennsylvania', 'electoral_votes': 19},
        {'name': 'Rhode Island', 'electoral_votes': 4},
        {'name': 'South Carolina', 'electoral_votes': 9},
        {'name': 'South Dakota', 'electoral_votes': 3},
        {'name': 'Tennessee', 'electoral_votes': 11},
        {'name': 'Texas', 'electoral_votes': 40},
        {'name': 'Utah', 'electoral_votes': 6},
        {'name': 'Vermont', 'electoral_votes': 3},
        {'name': 'Virginia', 'electoral_votes': 13},
        {'name': 'Washington', 'electoral_votes': 12},
        {'name': 'West Virginia', 'electoral_votes': 4},
        {'name': 'Wisconsin', 'electoral_votes': 10},
        {'name': 'Wyoming', 'electoral_votes': 3},
    ]

    states = {}
    for info in states_info:
        state = State(info['name'], info['electoral_votes'])
        states[info['name']] = state

    safe_states_harris = [
        'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
        'Hawaii', 'Illinois', 'Maine At-Large', 'Maine CD1', 'Maryland',
        'Massachusetts', 'Minnesota', 'New Jersey', 'New Mexico', 'New York',
        'Oregon', 'Rhode Island', 'Vermont', 'Virginia', 'Washington'
    ]

    safe_states_trump = [
        'Alabama', 'Alaska', 'Arkansas', 'Florida', 'Idaho', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Mississippi', 'Missouri', 'Montana',
        'Nebraska At-Large', 'Nebraska CD1', 'Nebraska CD3', 'North Dakota',
        'Ohio', 'Oklahoma', 'South Carolina', 'South Dakota', 'Tennessee',
        'Texas', 'Utah', 'West Virginia', 'Wyoming'
    ]

    for state_name in safe_states_harris:
        state = states[state_name]
        state.harris_support = 60.0 
        state.trump_support = 35.0
        state.std_dev = 2.0  

    for state_name in safe_states_trump:
        state = states[state_name]
        state.harris_support = 35.0
        state.trump_support = 60.0  
        state.std_dev = 2.0  

    competitive_states = [
        'Arizona', 'Georgia', 'Michigan', 'Nevada',
        'North Carolina', 'Pennsylvania', 'Wisconsin', 'Maine CD2', 'Nebraska CD2'
    ]


    # Arizona
    states['Arizona'].add_poll(harris_support=47, trump_support=51, weight=8, moe=3.0) #Atlas Intel
    states['Arizona'].add_poll(harris_support=42, trump_support=50, weight=7, moe=2.8) #Data Orbital
    states['Arizona'].add_poll(harris_support=42, trump_support=50, weight=7, moe=4.4) #CNN/SSRS
    states['Arizona'].add_poll(harris_support=49, trump_support=50, weight=7, moe=3.7) #Marist College
    states['Arizona'].add_poll(harris_support=46, trump_support=49, weight=8, moe=4.8) #WAPO

    # Georgia
    states['Georgia'].add_poll(harris_support=48, trump_support=51, weight=8, moe=3.0) #Atlas Intel
    states['Georgia'].add_poll(harris_support=49, trump_support=49, weight=7, moe=3.9) #Data Orbital
    states['Georgia'].add_poll(harris_support=48, trump_support=50, weight=8, moe=3.0) #Atlas Intel
    states['Georgia'].add_poll(harris_support=46, trump_support=52, weight=6, moe=2.7) #Quinnipiac University

    # Michigan
    states['Michigan'].add_poll(harris_support=48, trump_support=49, weight=8, moe=3.0) #Atlas Intel
    states['Michigan'].add_poll(harris_support=48, trump_support=43, weight=7, moe=4.7) #CNN/SSRS
    states['Michigan'].add_poll(harris_support=47, trump_support=46, weight=8, moe=3.7) #WAPO
    states['Michigan'].add_poll(harris_support=49, trump_support=49, weight=9, moe=3.0) #Beacon Research and Shaw
    states['Michigan'].add_poll(harris_support=52, trump_support=47, weight=7, moe=4.9) #Susquehanna
    states['Michigan'].add_poll(harris_support=47, trump_support=47, weight=7, moe=4.4) #Suffolk University
    states['Michigan'].add_poll(harris_support=49, trump_support=50, weight=7, moe=3.0) #Emerson College

    # Nevada
    states['Nevada'].add_poll(harris_support=48, trump_support=49, weight=8, moe=3.0) #Atlas Intel
    states['Nevada'].add_poll(harris_support=47, trump_support=48, weight=7, moe=2.7) #CNN/SSRS
    states['Nevada'].add_poll(harris_support=48, trump_support=48, weight=8, moe=3.0) #Atlas Intel
    states['Nevada'].add_poll(harris_support=48, trump_support=48, weight=8, moe=4.8) #WAPO
    states['Nevada'].add_poll(harris_support=43, trump_support=49, weight=6, moe=2.7) #WSJ
    states['Nevada'].add_poll(harris_support=49, trump_support=48, weight=7, moe=3.0) #Emerson College

    # North Carolina
    states['North Carolina'].add_poll(harris_support=49, trump_support=48, weight=8, moe=3.0) #Atlas Intel
    states['North Carolina'].add_poll(harris_support=49, trump_support=50, weight=9, moe=3.0) #Beacon Research and Shaw
    states['North Carolina'].add_poll(harris_support=45, trump_support=47, weight=7, moe=4.2) #Umass Lowell
    states['North Carolina'].add_poll(harris_support=48, trump_support=50, weight=7, moe=3.6) #Marist College
    states['North Carolina'].add_poll(harris_support=48, trump_support=50, weight=7, moe=3.1) #Emerson College
    states['North Carolina'].add_poll(harris_support=51, trump_support=49, weight=8, moe=3.0) #Atlas Intel
    states['North Carolina'].add_poll(harris_support=47, trump_support=50, weight=8, moe=3.9) #WAPO

    # Pennsylvania
    states['Pennsylvania'].add_poll(harris_support=50, trump_support=48, weight=7, moe=3.4) #Marist College
    states['Pennsylvania'].add_poll(harris_support=49, trump_support=49, weight=7, moe=4.4) #Suffolk College
    states['Pennsylvania'].add_poll(harris_support=48, trump_support=47, weight=8, moe=3.1) #WAPO
    states['Pennsylvania'].add_poll(harris_support=47, trump_support=50, weight=8, moe=3.0) #Atlas Intel
    states['Pennsylvania'].add_poll(harris_support=48, trump_support=48, weight=7, moe=4.7) #CNN/SSRS
    states['Pennsylvania'].add_poll(harris_support=49, trump_support=50, weight=9, moe=3.0) #Beacon Research and Shaw
    states['Pennsylvania'].add_poll(harris_support=47, trump_support=49, weight=7, moe=2.1) #Quinnipiac University
    states['Pennsylvania'].add_poll(harris_support=46, trump_support=47, weight=7, moe=3.8) #Monmouth University
    states['Pennsylvania'].add_poll(harris_support=48, trump_support=47, weight=7, moe=3.7) #Umass Lowell
    states['Pennsylvania'].add_poll(harris_support=46, trump_support=46, weight=7, moe=4.4) #Susquehanna
    states['Pennsylvania'].add_poll(harris_support=49, trump_support=51, weight=8, moe=3.3) #Emerson College
    states['Pennsylvania'].add_poll(harris_support=49, trump_support=50, weight=7, moe=3.0) #Franklin & Marshall College

    # Wisconsin
    states['Wisconsin'].add_poll(harris_support=49, trump_support=49, weight=8, moe=3.0) #Atlas Intel
    states['Wisconsin'].add_poll(harris_support=51, trump_support=45, weight=7, moe=4.8) #CNN/SSRS
    states['Wisconsin'].add_poll(harris_support=50, trump_support=49, weight=8, moe=3.0) #Marquette Law School
    states['Wisconsin'].add_poll(harris_support=47, trump_support=48, weight=7, moe=4.4) #Suffolk University
    states['Wisconsin'].add_poll(harris_support=49, trump_support=50, weight=8, moe=3.1) #Emerson College
    states['Wisconsin'].add_poll(harris_support=48, trump_support=48, weight=7, moe=2.9) #Quinnipiac University
    states['Wisconsin'].add_poll(harris_support=49, trump_support=48, weight=8, moe=3.0) #Atlas Intel
    states['Wisconsin'].add_poll(harris_support=50, trump_support=47, weight=8, moe=4.6) #WAPO

    # Maine CD2
    states['Maine CD2'].add_poll(harris_support=41, trump_support=50, weight=5, moe=3.0)

    # Nebraska CD2
    states['Nebraska CD2'].add_poll(harris_support=54, trump_support=42, weight=10, moe=3.0)

    for state_name in competitive_states:
        state = states[state_name]
        state.calculate_weighted_support()
        state.std_dev = 4.0

    simulations = 1000
    harris_wins = 0
    trump_wins = 0
    ties = 0

    for sim in range(simulations):
        harris_evs = 0
        trump_evs = 0
        for state in states.values():
            harris_margin = state.harris_support - state.trump_support
            harris_margin_result = random.gauss(harris_margin, state.std_dev)
            if harris_margin_result > 0:
                harris_evs += state.electoral_votes
            else:
                trump_evs += state.electoral_votes

        if harris_evs >= 270:
            harris_wins += 1
        elif trump_evs >= 270:
            trump_wins += 1
        else:
            ties += 1

    print(f"\nOut of {simulations} simulations:")
    print(f"Kamala Harris wins: {harris_wins} times")
    print(f"Donald Trump wins: {trump_wins} times")
    print(f"Ties or no majority: {ties} times")

if __name__ == '__main__':
    main()

