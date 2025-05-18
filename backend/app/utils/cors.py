from flask_cors import CORS
import os

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

def init_cors(app):
    CORS(app, 
         resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
