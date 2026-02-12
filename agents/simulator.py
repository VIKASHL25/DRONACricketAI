import math


def simulate_over(required_runs,
                  balls_left,
                  aggression=1.0,
                  batsman_runs=0,
                  balls_faced=1,
                  wickets_in_hand=6):

    if balls_left <= 0:
        return 0.0

    overs_left=balls_left/6
    rrr=required_runs/overs_left

    if balls_faced>0:
        strike_rate=(batsman_runs/balls_faced)*100
    else:
        strike_rate=120

    scoring_capacity=(strike_rate/100)*6
    pressure_ratio=rrr/scoring_capacity
    wicket_factor=wickets_in_hand/10
    aggression_factor=1+(aggression-1)*0.15
    pressure_penalty=math.exp(-pressure_ratio)

    win_prob=(
        pressure_penalty*
        wicket_factor*
        aggression_factor
    )

    if pressure_ratio > 3:
        win_prob*=0.1
    if pressure_ratio > 5:
        win_prob*=0.05
    if pressure_ratio > 7:
        win_prob*=0.01

    win_prob=max(0.0001, min(win_prob, 0.99))

    return round(win_prob, 4)
