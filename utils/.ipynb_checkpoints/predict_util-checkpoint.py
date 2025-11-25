import joblib
import pandas as pd

model = joblib.load("ml/productivity_model.pkl")

def predict_productivity(df_input: pd.DataFrame):
    data = df_input[
        ['focus_level', 'mood_level', 'overthinking_level', 'stress_level',
         'procrastination_level', 'sleep_hours', 'sleep_quality',
         'nap_taken', 'tasks_planned', 'tasks_done', 'distractions',
         'exercise_level', 'hydration_liters', 'junk_food_intake',
         'outside_food', 'body_energy', 'screen_time', 'doom_scrolling_time',
         'productivity_yesterday']
    ]
    prediction = model.predict(data)[0]
    return round(float(prediction), 2)

