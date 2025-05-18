# Đường dẫn: backend/app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from ..extensions import mongo

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Kiểm tra xem email đã tồn tại chưa
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"success": False, "message": "Email đã được sử dụng!"}), 400

    # Tạo người dùng mới
    user_data = {
        "email": email,
        "password": password  # Lưu trực tiếp password (không mã hóa)
    }
    mongo.db.users.insert_one(user_data)
    return jsonify({"success": True, "user": {"email": email}}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    print("Đang gọi API login")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Tìm người dùng theo email
    user = mongo.db.users.find_one({"email": email})

    # So sánh mật khẩu thuần túy
    if user and user['password'] == password:
        return jsonify({"success": True, "user": {"email": user['email']}}), 200
    else:
        return jsonify({"success": False, "message": "Đăng nhập thất bại!"}), 401
