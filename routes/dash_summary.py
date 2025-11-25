from fastapi import APIRouter
from firebase_config import get_db
from utils.ccharts import prod_health_line_chart, cat_score_bar_chart, task_ratio_chart, bmap_chart
from utils.summary import get_week_summary

router = APIRouter()

def get_user_data(user_id: str):
    """Helper function to fetch and preprocess user data."""
    rtdb = get_db()
    ref = rtdb.reference(f"users/{user_id}/logs")
    logs_raw = ref.get()

    if not logs_raw:
        return []

    data = []
    for date, entry in logs_raw.items():
        data.append({
            "date": date,
            "productivity": entry.get("productivity_score", 0),
            "health": entry.get("health_score", 0),
            "category_scores": entry.get("category_score", {}),
            "tasks_planned": entry.get("tasks_planned",0),
            "tasks_done": entry.get("tasks_done",0),
            "sleep_hours": entry.get("sleep_hours",0),
            "sleep_quality": entry.get("sleep_quality",0),
            "focus_level": entry.get("focus_level",0),
            "mood_level": entry.get("mood_level",0),
            "stress_level": entry.get("stress_level",0),
            "exercise_level": entry.get("exercise_level",0),
            "energy_level": entry.get("body_energy",0),
            "screen_time": entry.get("screen_time",0)
        })

    data = sorted(data, key=lambda x: x["date"])
    return data




@router.get("/last-log")
async def get_last_log(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"last_log": None}   
    latest_entry = data[-1]
    return {"last_log": latest_entry}


@router.get("/chart/bar")
async def get_bar_chart(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"chart": None}

    latest_entry = data[-1]
    category_scores = latest_entry.get("category_scores", {})

    category_scores = {
        "Mind & Focus": category_scores.get("Mind & Focus", 0),
        "Sleep": category_scores.get("Sleep", 0),
        "Physical Health": category_scores.get("Physical Health", 0),
        "Screen Habits": category_scores.get("Screen Habits", 0)
    }
    print(category_scores["Mind & Focus"])
    bar_chart = cat_score_bar_chart(category_scores)
    return {"chart": bar_chart}


@router.get("/chart/line")
async def get_line_chart(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"chart": None}

    week_data = data[-7:]
    line_chart = prod_health_line_chart(week_data)
    return {"chart": line_chart}


@router.get("/chart/stackchart")
async def get_heatmap(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"chart": None}

    week_data = data[-7:]
    stack_chart = task_ratio_chart(week_data)
    return {"chart": stack_chart}


@router.get("/chart/bmap_chart")
async def get_bmap_chart(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"chart": None}

    week_data = data[-7:]
    b_chart = bmap_chart(week_data)
    return {"chart": b_chart}


@router.get("/week_summary")
async def get_heatmap(user_id: str):
    data = get_user_data(user_id)
    if not data:
        return {"ws": None}

    week_data = data[-7:]
    week_summary = get_week_summary(week_data)
    return {"ws": week_summary}
