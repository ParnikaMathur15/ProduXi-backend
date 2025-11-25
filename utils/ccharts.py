import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io, base64
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded



def cat_score_bar_chart(category_scores):
    fig = plt.figure(figsize=(5, 4), constrained_layout=True)

    axis_color = "#2E1A2C"
    bar_color = "#8A4FFF"

    categories = list(category_scores.keys())
    scores = list(category_scores.values())

    plt.bar(categories, scores, color=bar_color, alpha=0.85)

    plt.xticks(rotation=30, fontsize=9, color=axis_color)
    plt.yticks(fontsize=9, color=axis_color)
    plt.grid(axis='y', alpha=0.25)

    plt.title("Well-being Scores", fontsize=11, color=axis_color)
    plt.xlabel("Domains", fontsize=9, color=axis_color)
    plt.ylabel("Score", fontsize=9, color=axis_color)

    y_max = max(scores) * 1.10
    plt.ylim(0, y_max)

    for i, val in enumerate(scores):
        plt.text(i, val + 1, f"{val:.1f}", ha='center', fontsize=8, color=axis_color)

    return fig_to_base64(fig)



def prod_health_line_chart(data):
    dates = [d["date"] for d in data]
    prod = [d["productivity"] for d in data]
    health = [d["health"] for d in data]

    fig = plt.figure(figsize=(5, 4), constrained_layout=True)

    productivity_color = "#8A4FFF" 
    health_color = "#FFBFA9"      
    axis_color = "#2E1A2C"          

    plt.plot(dates, prod, label="Productivity", linewidth=1.5, marker='o', color=productivity_color)
    plt.plot(dates, health, label="Health", linewidth=1.5, marker='o', color=health_color)

    plt.xticks(rotation=30, fontsize=9, color=axis_color)
    plt.yticks(fontsize=9, color=axis_color)
    plt.xlabel("Dates", fontsize=9, color=axis_color)
    plt.ylabel("Score", fontsize=9, color=axis_color)
    plt.grid(alpha=0.25)

    plt.title("Weekly Productivity & Health Trend", fontsize=11, color=axis_color)
    plt.legend()

    return fig_to_base64(fig)



def task_ratio_chart(data):     
    axis_color = "#2E1A2C" 

    fig = plt.figure(figsize=(6, 4.5), constrained_layout=True)
    dates = [d["date"] for d in data]
    tp = np.array([d["tasks_planned"] for d in data])
    td = np.array([d["tasks_done"] for d in data])

    incomplete = tp - td
    plt.bar(dates, td, color='#8A4FFF', label='Completed')
    plt.bar(dates, incomplete, bottom=td, color='#FFBFA9', label='Incomplete')

    plt.title("Task Completion Ratio", fontsize=13)
    plt.ylabel("Number of Tasks")
    plt.xlabel("Dates")
    plt.xticks(rotation=30, fontsize=9, color=axis_color)
    plt.yticks(fontsize=9, color=axis_color)
    plt.legend()
    plt.grid(alpha=0.2)

    return fig_to_base64(fig)



def bmap_chart(data):
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.sort_values("date")

    columns = ["focus_level", "stress_level", "sleep_hours", "sleep_quality", "exercise_level","energy_level", "screen_time"]

    labels = {
        "focus_level": "Focus",
        "stress_level": "Stress",
        "sleep_hours": "Sleep (hrs)",
        "sleep_quality": "Sleep Quality",
        "exercise_level": "Exercise",
        "energy_level": "Energy",
        "screen_time": "Screen Time (hrs)"
    }

    def convert_to_bucket(feature, value):
        if pd.isna(value):
            return 1 

        if feature in ["focus_level", "sleep_quality", "energy_level"]:
            if value <= 2: return 0
            elif value <= 3: return 1
            else: return 2

        if feature == "stress_level":
            if value >= 4: return 0
            elif value >= 2: return 1
            else: return 2

        if feature == "sleep_hours":
            if value < 5.5: return 0
            elif value <= 7.5: return 2
            else: return 1

        if feature == "exercise_level":
            if value == 0: return 0
            elif value == 1: return 1
            else: return 2

        if feature == "screen_time":
            if value > 6: return 0
            elif value > 3: return 1
            else: return 2

        return 1

    pattern = []
    for feature in columns:
        row = [convert_to_bucket(feature, v) for v in df[feature]]
        pattern.append(row)

    pattern = np.array(pattern)

    cmap = ListedColormap(["#D95F76", "#FFBFA9", "#8A4FFF"])

    fig, ax = plt.subplots(figsize=(9, 6))  
    ax.imshow(pattern, cmap=cmap, aspect="auto")

    ax.set_yticks(range(len(columns)))
    ax.set_yticklabels([labels[c] for c in columns], fontsize=12)

    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["date"], fontsize=12, rotation=45)

    ax.set_yticks(np.arange(-0.5, len(columns), 1), minor=True)
    ax.set_xticks(np.arange(-0.5, len(df), 1), minor=True)
    ax.grid(which="minor", color="black", linewidth=0.3)

    ax.set_title("Behavior Pattern Map", fontsize=14)

    red = mpatches.Patch(color="#D95F76", label="Needs Attention")
    peach = mpatches.Patch(color="#FFBFA9", label="Balanced")
    purple = mpatches.Patch(color="#8A4FFF", label="Going Well")

    fig.legend(
        handles=[red, peach, purple],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15),  
        ncol=3,
        frameon=False,
        fontsize=12,
    )
    return fig_to_base64(fig)

