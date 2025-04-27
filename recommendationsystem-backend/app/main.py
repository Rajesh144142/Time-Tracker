# app/main.py
from fastapi import FastAPI
from app.config import APP_NAME
from app.routes import assistant
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routes
app.include_router(assistant.router, prefix="/api")

@app.get("/")
def home():
    return {"message": f"{APP_NAME} is running 🚀"}
