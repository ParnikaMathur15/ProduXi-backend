import pandas as pd

def get_week_summary(data):
    n = len(data)
    df = pd.DataFrame(data)
    if n < 3:
        return ["Not enough weekly data to generate meaningful insights. Keep logging daily to unlock full weekly summaries!"]
    insights = []
    # ---- BASIC METRICS ----
    prod_mean = df["productivity"].mean()
    prod_std = df["productivity"].std()

    focus_mean = df["focus_level"].mean()
    print(focus_mean)
    stress_mean = df["stress_level"].mean()
    mood_mean = df["mood_level"].mean()
    sleeph_mean = df["sleep_hours"].mean()
    screen_mean = df["screen_time"].mean()

    sleepq_mode = df["sleep_quality"].mode()[0]
    energy_mode = df["energy_level"].mode()[0]

    # -------------------------------------------------------------
    #  PRODUCTIVITY INSIGHTS
    # -------------------------------------------------------------
    if prod_mean > 75:
        insights.append(f"Your productivity averaged {prod_mean:.1f}, which is exeptional for the week.")
    elif prod_mean > 60:
        insights.append(f"Your productivity this week was solid and steady  ({prod_mean:.1f}). You handled most days well and maintained a good rhythm.")
    else:
        insights.append(f"Your productivity was lower this week, {prod_mean:.1f} and that’s okay. It may help to gently explore whether sleep, stress, or mood affected your flow.")

    if prod_std < 5:
        insights.append("Your week was very consistent with minimal fluctuation in daily performance.")
    elif prod_std > 15:
        insights.append("Your productivity jumped up and down this week. This usually reflects emotional or environmental fluctuations — try grounding your days with one or two stabilizing habits.")
    else:
        insights.append("Your week had natural rises and dips — very normal for most people navigating multiple responsibilities.")

    # ---- WEEK PROGRESSION ----
    half = n // 2
    first_half = df["productivity"].iloc[:half].mean()
    second_half = df["productivity"].iloc[half:].mean()

    threshold = max(5, prod_std * 0.5)

    if second_half > first_half + threshold:
        insights.append("You ended the week stronger than you started, a great sign of momentum building!")
    elif second_half < first_half - threshold:
        insights.append("Your productivity seemed to dip towards the end of the week. It may help to pause and notice what shifted — sleep, stress, workload, or mood.")

    # ---- BEST/WORST DAY ----
    best_day = df['productivity'].idxmax()
    worst_day = df['productivity'].idxmin()

    insights.append(f"Your most productive day was {df.loc[best_day, 'date']} with a score of {df.loc[best_day, 'productivity']:.1f}, and your productivity was least on {df.loc[worst_day, 'date']} at {df.loc[worst_day, 'productivity']:.1f}. Exploring what felt different on those days may help you understand your patterns more deeply.")

    # ---- CORRELATION ANALYSIS ----
    try:
        corr = df.corr(numeric_only=True)["productivity"].drop("productivity").sort_values()

        top_neg = corr.index[0]
        top_pos = corr.index[-1]

        insights.append(
            f"{top_pos.replace('_', ' ')} had the strongest positive impact on your productivity, Maintaining it could create even more stability."
        )
        insights.append(
            f"{top_neg.replace('_', ' ')} had the most negative impact. A small adjustment here could boost next week’s performance."
        )
    except:
        insights.append("Not enough numeric data for correlation insights.")

    # -------------------------------------------------------------
    #  SLEEP HOURS
    # -------------------------------------------------------------
    if sleeph_mean < 6.0:
        insights.append("You slept less than your body likely needed. Even small improvements in sleep duration can uplift energy and emotional clarity.")
    elif sleeph_mean > 8.0:
        insights.append("You gave your body generous rest this week, a strong base that supports both mood and productivity.")

    # -------------------------------------------------------------
    #  FOCUS
    # -------------------------------------------------------------
    if focus_mean > 4.0:
        insights.append("You maintained great focus throughout the week that's a major contributor to your productivity.")
    elif focus_mean < 2.5:
        insights.append("Your focus felt challenged on many days. Gentle reductions in distractions could help you regain your mental space.")
    else:
        insights.append("Your focus levels were moderate and fairly steady, consistent performance overall.")

    # -------------------------------------------------------------
    #  STRESS
    # -------------------------------------------------------------
    if stress_mean > 4.0:
        insights.append("Your stress levels were heavy this week. It may help to build in small calming rituals — breathing, quiet breaks, or walks.")
    elif stress_mean < 2.0:
        insights.append("You carried yourself with calmness most days, a wonderful strength that supports long-term wellbeing.")

    # -------------------------------------------------------------
    #  MOOD
    # -------------------------------------------------------------
    if mood_mean > 4.0:
        insights.append("Your mood stayed uplifting most of the week, emotional stability played a big role in your productivity.")
    elif mood_mean < 2.5:
        insights.append("Your mood felt low on several days. It might be helpful to reflect gently on what felt heavy or overwhelming.")

    # -------------------------------------------------------------
    #  SCREEN TIME
    # -------------------------------------------------------------
    if screen_mean > 6.0:
        insights.append("Your screen time was quite high, it has affected your sleep and focus.")
    elif screen_mean > 4.0:
        insights.append("Your screen time was moderately high, reducing it could improve mental clarity.")
    elif screen_mean > 2.0:
        insights.append("Your screen habits were balanced this week, good job maintaining discipline.")
    
    # -------------------------------------------------------------
    #  SLEEP QUALITY
    # -------------------------------------------------------------
    if sleepq_mode <= 2.0:
        insights.append("Sleep quality felt low on most days. Improving wind-down routines could help you feel more refreshed!")
    elif sleepq_mode == 3.0:
        insights.append("Your sleep quality was moderate, a few small improvements could give you a noticeable boost!")
    
    # -------------------------------------------------------------
    #  ENERGY
    # -------------------------------------------------------------
    if energy_mode <= 2.0:
        insights.append("Your energy was low on many days. Better rest, hydration, and movement might help restore vitality.")
    elif energy_mode == 3.0:
        insights.append("Your energy was generally stable but with room for improvement, small boosts could make next week smoother.")
    elif energy_mode>3:
        insights.append("You carried strong energy through the week, a wonderful sign of good physical and mental alignment.")

    return insights
