from flask import Blueprint, request, jsonify, redirect, url_for

chat_bp = Blueprint("chat", __name__)

# Đăng xuất người dùng (sử dụng @app.route nếu bạn có Flask app chính để đăng ký route này)
@chat_bp.route('/logout', methods=['GET'])
def logout():
    # Đăng xuất người dùng
    return redirect(url_for('login'))  # Giả sử bạn có route 'login' đã được đăng ký

# Route xử lý message của chatbot
@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Xử lý thông điệp người dùng và trả lời chatbot
    bot_response = f"Bot trả lời: {user_message}"  # Logic trả lời chatbot có thể phức tạp hơn
    
    return jsonify({
        "bot": bot_response
    })
