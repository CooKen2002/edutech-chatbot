# db.py
from flask_mongoengine import MongoEngine
import logging

db = MongoEngine()

def init_db(app):
    try:
        db.init_app(app)
        app.logger.info("Kết nối MongoDB thành công!")
    except Exception as e:
        app.logger.error(f"Kết nối MongoDB thất bại: {e}")
