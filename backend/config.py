# backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key"
    MONGODB_SETTINGS = {
        "db": os.environ.get("DATABASE_NAME") or "edutech_chatbot",  # Đảm bảo tên database là chatbot_db
        "host": os.environ.get("MONGO_URI") or "mongodb://localhost:27017/edutech_chatbot",  # Kết nối đúng URI MongoDB
    }

