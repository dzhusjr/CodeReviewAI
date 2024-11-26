from fastapi import FastAPI
import logging
from app.routes import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler("app.log")
    ],
)

app = FastAPI(
    title="CodeReviewAI",
    description="An API to auto-review coding assignments using OpenAI and GitHub",
    version="1.0.0",
)

app.include_router(router)
