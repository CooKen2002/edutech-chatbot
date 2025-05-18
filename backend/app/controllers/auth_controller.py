# backend/app/controllers/auth_controller.py

from flask import jsonify, request
from app.models.chatlog import User  # Import model User trực tiếp từ chatlog

def register_user(email, password):
    # Kiểm tra người dùng đã tồn tại chưa
    if User.objects(email=email).first():
        return jsonify({"message": "Người dùng đã tồn tại"}), 400
    
    # Tạo người dùng mới
    user = User(email=email, password=password)
    user.save()
    return jsonify({"message": "Đăng ký thành công"}), 201

def login_user(email, password):
    user = User.objects(email=email).first()
    
    if not user or user.password != password:
        return jsonify({"message": "Thông tin đăng nhập không chính xác"}), 401
    
    return jsonify({"message": "Đăng nhập thành công"}), 200
