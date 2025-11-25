from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.submit_form import router as submit_router
from routes.avg_scores import router as scores_router
from routes.dash_summary import router as dash_summary_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submit_router)
app.include_router(scores_router)
app.include_router(dash_summary_router)