# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from .extensions import mongo
from .routes.auth_routes import auth_bp
from .routes.chat_routes import chat_bp
from .routes.user_routes import user_bp
from .routes.course_routes import course_bp
def create_app():
    app = Flask(__name__)

    # Cấu hình MongoDB với PyMongo
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/edutech_chatbot'
    
    mongo.init_app(app)  # Khởi tạo mongo với Flask app
    

    try:
        with app.app_context():
            db_name = mongo.db.name
            print(f"✅ Đã kết nối tới MongoDB: {db_name}")
    except Exception as e:
        print(f"❌ Kết nối MongoDB thất bại: {str(e)}")
        
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    # Đăng ký các blueprint
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(course_bp, url_prefix="/api/course")
    
    return app
