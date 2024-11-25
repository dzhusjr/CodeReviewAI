from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="CodeReviewAI",
    description="An API to auto-review coding assignments using OpenAI and GitHub",
    version="1.0.0",
)

app.include_router(router)
