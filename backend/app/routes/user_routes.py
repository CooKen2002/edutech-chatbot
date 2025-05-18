from flask import Blueprint, request, jsonify
from ..services.user_service import get_user_info, update_user_info
from ..models.progress import get_all_progress_by_user, progress_collection
from ..models.course import courses_collection
from ..models.user import users_collection
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/user-info', methods=['GET'])
def get_user_information():
    email = request.args.get('email', '').strip()
    if not email:
        return jsonify({"success": False, "message": "Vui lòng cung cấp email."}), 400

    user = get_user_info(email)
    if user:
        return jsonify({
            "success": True,
            "data": {
                "email": user.get("email"),
                "learning_progress": user.get("learning_progress"),
                "interests": user.get("interests"),
                "learning_path": user.get("learning_path"),
                "hobby": user.get("hobby"),
                "subj": user.get("subj")
            }
        }), 200

    return jsonify({"success": False, "message": "Không tìm thấy thông tin người dùng."}), 404


@user_bp.route('/update-profile', methods=['POST'])
def update_profile():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        update_fields = data.get('preferences') or data.get('update_fields') or {}

        if not email or not update_fields:
            return jsonify({"success": False, "message": "Thiếu thông tin yêu cầu"}), 400

        user = get_user_info(email)
        if not user:
            return jsonify({"success": False, "message": "Người dùng không tồn tại"}), 404

        # Cập nhật root fields
        result = update_user_info(email, update_fields)
        if result.modified_count > 0:
            user = get_user_info(email)
            return jsonify({"success": True, "message": "Cập nhật thành công", "data": user}), 200
        else:
            return jsonify({"success": False, "message": "Không có trường nào thay đổi"}), 200

    except Exception as e:
        print(f"[ERROR] Exception in update_profile: {str(e)}")
        return jsonify({"success": False, "message": "Lỗi server"}), 500

@user_bp.route("/user-progress", methods=["GET"])
def get_learning_progress():
    email = request.args.get("email", "").strip()
    if not email:
        return jsonify({"success": False, "message": "Thiếu email"}), 400

    # Kiểm tra user tồn tại
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404

    # Lấy danh sách tiến độ học từ collection progress
    progress_list = list(progress_collection.find({"user_email": email}))

    results = []
    for item in progress_list:
        course_name = item.get("course_name")
        progress_percent = item.get("completion_percent", 0)

        # Tìm thông tin khóa học trong courses_collection
        course = courses_collection.find_one({"name": course_name})
        if course:
            results.append({
                "id": str(course["_id"]),
                "name": course["name"],
                "status": "Đang học",
                "progress": progress_percent
            })

    return jsonify({"success": True, "data": results})
