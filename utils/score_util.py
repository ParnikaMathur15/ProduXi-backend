import pandas as pd
def normalize(val, min_val, max_val):
    return max(0, min((val - min_val) / (max_val - min_val), 1))

def invert_normalize(val, min_val, max_val):
    return 1 - normalize(val, min_val, max_val)

def calculate_health_score(df_input: pd.DataFrame):
    form_df=df_input.iloc[0]

    mind_focus_inputs = [
        normalize(form_df['focus_level'], 1, 5),
        normalize(form_df['mood_level'], 1, 5),
        invert_normalize(form_df['overthinking_level'], 0, 3),
        invert_normalize(form_df['stress_level'], 1, 5),
        invert_normalize(form_df['procrastination_level'], 0, 2)
    ]
    mind_score = sum(mind_focus_inputs) / len(mind_focus_inputs)

    sleep_inputs = [
        normalize(form_df['sleep_hours'], 0, 24),
        normalize(form_df['sleep_quality'], 1, 5),
        0.8 if form_df['nap_taken'] == 1 else 0.5
    ]
    sleep_score = sum(sleep_inputs) / len(sleep_inputs)

    physical_health_inputs = [
        form_df['exercise_level'],
        normalize(form_df['hydration_liters'], 2, 5),
        invert_normalize(form_df['junk_food_intake'], 0, 3),
        0.7 if form_df['outside_food'] == 0 else 0.4,
        normalize(form_df['body_energy'], 1, 5)
    ]
    physical_health_score = sum(physical_health_inputs) / len(physical_health_inputs)

    screen_habits_inputs = [
        invert_normalize(form_df['screen_time'], 0, 24),
        invert_normalize(form_df['doom_scrolling_time'], 0, 6)
    ]
    screen_habits_score = sum(screen_habits_inputs) / len(screen_habits_inputs)

    weights = {
        'Sleep': 0.4,
        'Physical Health': 0.4,
        'Screen Habits': 0.2
    }

    scores = {
        'Mind & Focus': mind_score,
        'Sleep': sleep_score,
        'Physical Health': physical_health_score,
        'Screen Habits': screen_habits_score
    }

    final_score = sum(scores[domain] * weights[domain] for domain in weights) * 100
    raw_scores_percent = {domain: round(scores[domain] * 100, 2) for domain in scores}

    if final_score>=75:
        rating="Excellent"        
    elif final_score>=50:
        rating="Stable"
    elif final_score>=25:
        rating="Needs Improvement"
    else:
        rating="Critical"

    return (round(final_score, 2), raw_scores_percent, rating)