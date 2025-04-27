# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Ticket Assistant")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
