import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Cấu hình chung cho ứng dụng"""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Kiểm tra xem có bật DEBUG không
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Secret key cho bảo mật
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # URI kết nối MongoDB
    DATABASE_NAME = os.getenv("DATABASE_NAME", "edutech_chatbot")  # Tên cơ sở dữ liệu MongoDB
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "superjwtsecret")  # Secret key cho JWT
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRES", 3600))  # Thời gian hết hạn của token (1 giờ mặc định)
    ENV = os.getenv("FLASK_ENV", "development")  # Môi trường của Flask (development hoặc production)

# Các cấu hình cho môi trường phát triển và sản xuất
class DevelopmentConfig(Config):
    DEBUG = True  # Bật Debug cho môi trường phát triển

class ProductionConfig(Config):
    DEBUG = False  # Tắt Debug cho môi trường sản xuất

# Định nghĩa cấu hình cho từng môi trường
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
