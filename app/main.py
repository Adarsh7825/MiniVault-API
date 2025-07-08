from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="MiniVault API",
    description="A lightweight API for prompt-response generation.",
    version="1.0.0"
)

app.include_router(router)
