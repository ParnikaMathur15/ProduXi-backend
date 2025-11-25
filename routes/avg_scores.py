from fastapi import APIRouter
from firebase_config import get_db

router = APIRouter()

@router.get("/avg-scores")
async def get_avg_scores(user_id: str):
    rtdb = get_db()
    ref = rtdb.reference(f"users/{user_id}/logs")
    logs_raw = ref.get()

    if not logs_raw:
        return {"productivity_avg": 0, "health_avg": 0}

    data = []
    for date, entry in logs_raw.items():
        data.append({
            "date": date,
            "health": entry.get("health_score", 0),
            "productivity": entry.get("productivity_score", 0)
        })

    data = sorted(data, key=lambda x: x["date"])
    last_7 = data[-7:]

    health_avg = sum(d["health"] for d in last_7) / len(last_7)
    prod_avg = sum(d["productivity"] for d in last_7) / len(last_7)

    return {
        "health_avg": round(health_avg, 2),
        "productivity_avg": round(prod_avg, 2),
    }
