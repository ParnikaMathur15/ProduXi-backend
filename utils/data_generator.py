import random
import pandas as pd
import numpy as np

personas = {
    "CEO": {
        "focus": (4, 1), "mood": (4, 1), "overthinking": [0, 1],
        "stress": (3, 1), "procrastination": [0, 1],
        "sleep_hours": (6, 1), "sleep_quality": (3, 1), "nap_taken": [0],
        "tasks_planned": (6, 2), "tasks_done_ratio": (0.9, 0.1), "distractions": (1, 1),
        "exercise": [1], "hydration": (3, 0.5), "junk_food": (1, 1),
        "outside_food": [0], "body_energy": (4, 1),
        "screen_time": (4, 1), "doom_scroll": (1, 1)
    },
    "Student": {
        "focus": (2.5, 1), "mood": (3, 1.2), "overthinking": [1, 2],
        "stress": (3.5, 1), "procrastination": [1, 2],
        "sleep_hours": (6.5, 1.5), "sleep_quality": (2.5, 1), "nap_taken": [0, 1],
        "tasks_planned": (4, 2), "tasks_done_ratio": (0.7, 0.2), "distractions": (2, 1),
        "exercise": [0, 1], "hydration": (2.5, 0.7), "junk_food": (2, 1),
        "outside_food": [1], "body_energy": (3, 1),
        "screen_time": (6, 1.5), "doom_scroll": (2, 1)
    },
    "Night Owl": {
        "focus": (2.5, 1), "mood": (2.5, 1), "overthinking": [2, 3],
        "stress": (3.5, 1), "procrastination": [2],
        "sleep_hours": (5, 1), "sleep_quality": (2, 1), "nap_taken": [1],
        "tasks_planned": (3, 1), "tasks_done_ratio": (0.6, 0.2), "distractions": (2, 1),
        "exercise": [0], "hydration": (2, 0.5), "junk_food": (2.5, 0.8),
        "outside_food": [1], "body_energy": (2.5, 1),
        "screen_time": (7, 1), "doom_scroll": (3, 1)
    },
    "Health Conscious": {
        "focus": (4, 1), "mood": (4, 1), "overthinking": [0, 1],
        "stress": (2, 1), "procrastination": [0, 1],
        "sleep_hours": (7.5, 1), "sleep_quality": (4, 1), "nap_taken": [0],
        "tasks_planned": (5, 1), "tasks_done_ratio": (0.85, 0.1), "distractions": (1, 1),
        "exercise": [2], "hydration": (3.5, 0.5), "junk_food": (0.5, 0.5),
        "outside_food": [0], "body_energy": (4.5, 0.5),
        "screen_time": (3.5, 1), "doom_scroll": (0.5, 0.5)
    },
    "Burnout Case": {
        "focus": (1.5, 1), "mood": (2, 1), "overthinking": [3],
        "stress": (4.5, 1), "procrastination": [2],
        "sleep_hours": (5, 1), "sleep_quality": (2, 1), "nap_taken": [1],
        "tasks_planned": (3, 1), "tasks_done_ratio": (0.4, 0.2), "distractions": (3, 0.5),
        "exercise": [0], "hydration": (1.5, 0.5), "junk_food": (3, 0.5),
        "outside_food": [1], "body_energy": (2, 1),
        "screen_time": (7, 1), "doom_scroll": (3, 1)
    },
    "Balanced Professional": {
        "focus": (3.5, 1), "mood": (3.5, 1), "overthinking": [1],
        "stress": (2.5, 1), "procrastination": [1],
        "sleep_hours": (7, 1), "sleep_quality": (3.5, 1), "nap_taken": [0, 1],
        "tasks_planned": (5, 1), "tasks_done_ratio": (0.8, 0.1), "distractions": (1.5, 1),
        "exercise": [1, 2], "hydration": (3, 0.5), "junk_food": (1, 1),
        "outside_food": [0, 1], "body_energy": (4, 1),
        "screen_time": (5, 1), "doom_scroll": (1.5, 1)
    },
    "Social Butterfly": {
        "focus": (2.5, 1), "mood": (4, 1), "overthinking": [1],
        "stress": (2.5, 1), "procrastination": [1],
        "sleep_hours": (6, 1), "sleep_quality": (3, 1), "nap_taken": [0, 1],
        "tasks_planned": (4, 1), "tasks_done_ratio": (0.75, 0.1), "distractions": (2, 1),
        "exercise": [1], "hydration": (2.5, 0.7), "junk_food": (2, 1),
        "outside_food": [1], "body_energy": (3.5, 1),
        "screen_time": (6, 1), "doom_scroll": (2, 1)
    },
    "Anxious Thinker": {
        "focus": (2, 1), "mood": (2.5, 1), "overthinking": [2, 3],
        "stress": (4, 1), "procrastination": [2],
        "sleep_hours": (6, 1.2), "sleep_quality": (2.5, 1), "nap_taken": [1],
        "tasks_planned": (4, 1), "tasks_done_ratio": (0.6, 0.15), "distractions": (2.5, 0.7),
        "exercise": [0, 1], "hydration": (2, 0.6), "junk_food": (2, 1),
        "outside_food": [1], "body_energy": (2.5, 1),
        "screen_time": (5.5, 1), "doom_scroll": (2.5, 1)
    }
}

def sample_discrete(choices):
    return random.choice(choices)

def generate_entry(persona_name):
    p = personas[persona_name]
    entry = {
        "focus_level": round(np.clip(np.random.normal(*p["focus"]), 1, 5)),
        "mood_level": round(np.clip(np.random.normal(*p["mood"]), 1, 5)),
        "overthinking_level": sample_discrete(p["overthinking"]),
        "stress_level": round(np.clip(np.random.normal(*p["stress"]), 1, 5)),
        "procrastination_level": sample_discrete(p["procrastination"]),
        "sleep_hours": round(np.clip(np.random.normal(*p["sleep_hours"]), 3, 10), 1),
        "sleep_quality": round(np.clip(np.random.normal(*p["sleep_quality"]), 1, 5)),
        "nap_taken": sample_discrete(p["nap_taken"]),
        "tasks_planned": max(1, int(np.random.normal(*p["tasks_planned"]))),
    }
    # Tasks done based on planned × ratio
    ratio = np.clip(np.random.normal(*p["tasks_done_ratio"]), 0.3, 1.0)
    entry["tasks_done"] = min(entry["tasks_planned"], int(round(entry["tasks_planned"] * ratio)))

    entry.update({
        "distractions": round(np.clip(np.random.normal(*p["distractions"]), 0, 3)),
        "exercise_level": sample_discrete(p["exercise"]),
        "hydration_liters": round(np.clip(np.random.normal(*p["hydration"]), 0.5, 5), 1),
        "junk_food_intake": round(np.clip(np.random.normal(*p["junk_food"]), 0, 3)),
        "outside_food": sample_discrete(p["outside_food"]),
        "body_energy": round(np.clip(np.random.normal(*p["body_energy"]), 1, 5)),
        "screen_time": round(np.clip(np.random.normal(*p["screen_time"]), 2, 10), 1),
        "doom_scrolling_time": round(np.clip(np.random.normal(*p["doom_scroll"]), 0, 4), 1),
        "productivity_yesterday": round(random.uniform(20, 95), 2) if random.random() < 0.8 else None,
        "user_id": persona_name
    })

    for key in ["focus_level", "mood_level", "sleep_hours", "tasks_done", "body_energy"]:
        if random.random() < 0.05:
            entry[key] = np.nan

    # Introduce rare outliers (1% chance per key)
    if random.random() < 0.01:
        entry["screen_time"] = round(random.uniform(12, 18), 1)  # extreme high screen time
    if random.random() < 0.01:
        entry["tasks_done"] = -1  # impossible negative tasks

    return entry

def calculate_productivity_score(row):
    try:
        focus = row["focus_level"]
        mood = row["mood_level"]
        overthinking = row["overthinking_level"]
        stress = row["stress_level"]
        procrastination = row["procrastination_level"]
        sleep = row["sleep_hours"]
        sleep_q = row["sleep_quality"]
        nap = row["nap_taken"]
        tasks_planned = row["tasks_planned"]
        tasks_done = row["tasks_done"]
        distractions = row["distractions"]
        exercise = row["exercise_level"]
        hydration = row["hydration_liters"]
        junk_food = row["junk_food_intake"]
        outside_food = row["outside_food"]
        energy = row["body_energy"]
        screen = row["screen_time"]
        doom = row["doom_scrolling_time"]
        yesterday = row["productivity_yesterday"]

        mind = (focus + mood - overthinking - stress - procrastination + 5) / 10
        sleep_score = (sleep_q + (7 - abs(7 - sleep))) / 10
        physical = (exercise + energy + hydration - junk_food - outside_food + 5) / 10
        effort = tasks_done / tasks_planned if tasks_planned else 0.5
        screen_score = (6 - screen + 3 - doom) / 10
        score = (
            0.25 * mind +
            0.2 * sleep_score +
            0.2 * physical +
            0.15 * effort +
            0.1 * screen_score +
            0.1 * (yesterday / 100 if pd.notna(yesterday) else 0.6)
        )

        if effort < 0.5:
            score -= 0.1
        if screen < 0.3:
            score += 0.05
        if overthinking == 3 and stress >= 4:
            score -= 0.15
        if sleep < 4:
            score -= 0.1
        if doom > 2.5:
            score -= 0.1

        if pd.notna(yesterday):
            if yesterday < 50:
                score -= 0.05
            elif yesterday > 80:
                score += 0.03

        score = max(min(score, 0.95), 0.3)
        return round(score * 100, 2)
    except Exception as e:
        return 50.0

def data_generation():
    entries = []
    persona_list = list(personas.keys())
    while len(entries) < 15000:
        for persona in persona_list:
            entries.append(generate_entry(persona))
            if len(entries) >= 15000:
                break

    df = pd.DataFrame(entries)

    # -------------------- START REALISM MODULES (Option A) --------------------
    df["day_of_week"] = np.random.randint(0, 7, size=len(df))
    weekend_mask = df["day_of_week"].isin([5, 6])

    # --- FIX NaN TASKS_DONE BEFORE WEEKEND LOGIC ---
    df["tasks_done"] = df["tasks_done"].fillna(
        (df["tasks_planned"] * np.random.uniform(0.2, 0.7)).round()
    )

    # --- WEEKEND EFFECT (Correct + Safe) ---
    # operate only on non-null tasks_done
    mask_weekend_tasks = df.loc[weekend_mask, "tasks_done"].notna()
    if mask_weekend_tasks.sum() > 0:
        idx_weekend = df.loc[weekend_mask].index[mask_weekend_tasks.values]
        df.loc[idx_weekend, "tasks_done"] = (
            df.loc[idx_weekend, "tasks_done"]
            * np.random.uniform(0.3, 0.8, size=len(idx_weekend))
        ).round().astype(int)

    # reduce planned tasks on weekends (safe)
    mask_weekend_planned = df.loc[weekend_mask, "tasks_planned"].notna()
    if mask_weekend_planned.sum() > 0:
        idx_weekend_planned = df.loc[weekend_mask].index[mask_weekend_planned.values]
        df.loc[idx_weekend_planned, "tasks_planned"] = (
            df.loc[idx_weekend_planned, "tasks_planned"]
            * np.random.uniform(0.4, 0.8, size=len(idx_weekend_planned))
        ).round().astype(int)

    # Adjust stress & screen time (safe)
    mask_weekend_stress = df.loc[weekend_mask, "stress_level"].notna()
    if mask_weekend_stress.sum() > 0:
        idx_weekend_stress = df.loc[weekend_mask].index[mask_weekend_stress.values]
        df.loc[idx_weekend_stress, "stress_level"] = np.clip(
            df.loc[idx_weekend_stress, "stress_level"]
            * np.random.uniform(0.7, 0.95, size=len(idx_weekend_stress)),
            1, 5
        ).round().astype(int)

    mask_weekend_screen = df.loc[weekend_mask, "screen_time"].notna()
    if mask_weekend_screen.sum() > 0:
        idx_weekend_screen = df.loc[weekend_mask].index[mask_weekend_screen.values]
        df.loc[idx_weekend_screen, "screen_time"] = np.clip(
            df.loc[idx_weekend_screen, "screen_time"]
            * np.random.uniform(1.0, 1.4, size=len(idx_weekend_screen)),
            0, 24
        )

    # --------- Rest of realism modules (kept exactly as you wrote) ---------

    deadline_idx = df.sample(frac=0.06, random_state=42).index
    # stress_level safe assign
    mask_deadline_stress = df.loc[deadline_idx, "stress_level"].notna()
    if mask_deadline_stress.sum() > 0:
        idx_deadline_stress = df.loc[deadline_idx].index[mask_deadline_stress.values]
        df.loc[idx_deadline_stress, "stress_level"] = np.clip(
            np.random.randint(4, 6, size=len(idx_deadline_stress)), 1, 5
        )

    # push tasks_done up safely (vectorized, only for rows with tasks_planned not null)
    sub = df.loc[deadline_idx].copy()
    mask_sub = sub["tasks_planned"].notna()
    if mask_sub.sum() > 0:
        idx_sub = sub.index[mask_sub.values]
        new_done = (sub.loc[mask_sub, "tasks_planned"] * np.random.uniform(0.9, 1.15, size=mask_sub.sum())).round().astype(int)
        capped = np.minimum(sub.loc[mask_sub, "tasks_planned"].astype(int), new_done)
        df.loc[idx_sub, "tasks_done"] = capped

    mask_deadline_body = df.loc[deadline_idx, "body_energy"].notna()
    if mask_deadline_body.sum() > 0:
        idx_deadline_body = df.loc[deadline_idx].index[mask_deadline_body.values]
        df.loc[idx_deadline_body, "body_energy"] = np.clip(
            np.random.randint(3, 6, size=len(idx_deadline_body)), 1, 5
        )

    num_patches = 5
    max_len = 6
    starts = np.random.choice(len(df), size=num_patches, replace=False)
    for s in starts:
        e = min(s + np.random.randint(2, max_len), len(df) - 1)
        idx = range(s, e + 1)

        # tasks_done patch (safe)
        mask_idx_tasks = df.loc[idx, "tasks_done"].notna()
        if mask_idx_tasks.sum() > 0:
            idx_tasks = df.loc[idx].index[mask_idx_tasks.values]
            df.loc[idx_tasks, "tasks_done"] = (
                df.loc[idx_tasks, "tasks_done"]
                * np.random.uniform(0.1, 0.4, size=len(idx_tasks))
            ).round().astype(int)

        # mood_level patch (safe)
        mask_idx_mood = df.loc[idx, "mood_level"].notna()
        if mask_idx_mood.sum() > 0:
            idx_mood = df.loc[idx].index[mask_idx_mood.values]
            arr = df.loc[idx_mood, "mood_level"] * np.random.uniform(0.4, 0.7, size=len(idx_mood))
            arr = np.clip(arr, 1, 5)
            df.loc[idx_mood, "mood_level"] = arr.round().astype(int)

        # stress_level patch (safe)
        mask_idx_stress = df.loc[idx, "stress_level"].notna()
        if mask_idx_stress.sum() > 0:
            idx_stress = df.loc[idx].index[mask_idx_stress.values]
            arr_s = df.loc[idx_stress, "stress_level"] * np.random.uniform(1.0, 1.4, size=len(idx_stress))
            arr_s = np.clip(arr_s, 1, 5)
            df.loc[idx_stress, "stress_level"] = arr_s.round().astype(int)

    swing_idx = df.sample(frac=0.03, random_state=7).index
    df.loc[swing_idx, "mood_level"] = np.random.randint(1, 6, size=len(swing_idx))
    df.loc[swing_idx, "overthinking_level"] = np.random.randint(0, 4, size=len(swing_idx))
    df.loc[swing_idx, "body_energy"] = np.random.randint(1, 6, size=len(swing_idx))

    drift_strength = np.random.normal(0.0, 0.15, size=len(df))
    # sleep_hours safe update (works with NaN)
    mask_sleep = df["sleep_hours"].notna()
    if mask_sleep.sum() > 0:
        df.loc[mask_sleep, "sleep_hours"] = np.clip(
            df.loc[mask_sleep, "sleep_hours"] + drift_strength[mask_sleep] * np.random.uniform(-0.5, 0.5, size=mask_sleep.sum()),
            2, 14
        ).round(1)

    # screen_time drift (safe)
    mask_screen = df["screen_time"].notna()
    if mask_screen.sum() > 0:
        df.loc[mask_screen, "screen_time"] = np.clip(
            df.loc[mask_screen, "screen_time"] + drift_strength[mask_screen] * np.random.uniform(-1, 1, size=mask_screen.sum()),
            0, 24
        ).round(1)

    # hydration drift (safe)
    mask_hyd = df["hydration_liters"].notna()
    if mask_hyd.sum() > 0:
        df.loc[mask_hyd, "hydration_liters"] = np.clip(
            df.loc[mask_hyd, "hydration_liters"] + drift_strength[mask_hyd] * np.random.uniform(-0.3, 0.3, size=mask_hyd.sum()),
            0.2, 6
        ).round(1)

    bad_day_idx = df.sample(frac=0.02, random_state=99).index
    df.loc[bad_day_idx, ["focus_level", "mood_level", "body_energy"]] = \
        np.random.randint(1, 3, size=(len(bad_day_idx), 3))
    df.loc[bad_day_idx, "tasks_done"] = np.random.randint(0, 2, size=len(bad_day_idx)).astype(int)
    mask_bad_screen = df.loc[bad_day_idx, "screen_time"].notna()
    if mask_bad_screen.sum() > 0:
        idx_bad_screen = df.loc[bad_day_idx].index[mask_bad_screen.values]
        df.loc[idx_bad_screen, "screen_time"] = np.clip(
            df.loc[idx_bad_screen, "screen_time"]
            * np.random.uniform(1.2, 2.0, size=len(idx_bad_screen)),
            0, 24
        )

    mistake_idx = df.sample(frac=0.01, random_state=123).index
    df.loc[mistake_idx, "nap_taken"] = 2

    tail_idx = df.sample(frac=0.01, random_state=21).index
    mask_tail_screen = df.loc[tail_idx, "screen_time"].notna()
    if mask_tail_screen.sum() > 0:
        idx_tail_screen = df.loc[tail_idx].index[mask_tail_screen.values]
        df.loc[idx_tail_screen, "screen_time"] = np.round(
            np.random.pareto(a=2.0, size=len(idx_tail_screen)) * 6 + 6, 1
        )
    mask_tail_junk = df.loc[tail_idx, "junk_food_intake"].notna()
    if mask_tail_junk.sum() > 0:
        idx_tail_junk = df.loc[tail_idx].index[mask_tail_junk.values]
        df.loc[idx_tail_junk, "junk_food_intake"] = np.clip(
            np.random.poisson(lam=3, size=len(idx_tail_junk)), 0, 10
        )

    df["tasks_planned"] = df["tasks_planned"].apply(
        lambda x: max(1, int(x)) if not pd.isna(x) else x
    )
    df["tasks_done"] = df["tasks_done"].apply(
        lambda x: int(max(0, round(x))) if not pd.isna(x) else x
    )

    # final clipping & safe int casting where needed (do not cast NaNs)
    for col, lo, hi, as_int in [
        ("focus_level", 1, 5, True),
        ("mood_level", 1, 5, True),
        ("stress_level", 1, 5, True),
        ("sleep_hours", 2, 14, False),
        ("sleep_quality", 1, 5, True),
        ("hydration_liters", 0.2, 6, False),
        ("body_energy", 1, 5, True),
        ("screen_time", 0, 24, False),
        ("doom_scrolling_time", 0, 6, False),
    ]:
        mask_col = df[col].notna()
        if mask_col.sum() > 0:
            if as_int:
                df.loc[mask_col, col] = df.loc[mask_col, col].clip(lo, hi).round().astype(int)
            else:
                df.loc[mask_col, col] = df.loc[mask_col, col].clip(lo, hi).round(1)

    # -------------------- END REALISM MODULES --------------------

    duplicates = df.sample(frac=0.02)
    df = pd.concat([df, duplicates], ignore_index=True)

    df = df.sample(frac=1).reset_index(drop=True)
    df["productivity_tomorrow"] = df.apply(calculate_productivity_score, axis=1)

    return df
