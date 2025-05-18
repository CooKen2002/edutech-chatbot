from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from ..models.course import get_course_by_id

course_bp = Blueprint("course_bp", __name__, url_prefix="/course")

@course_bp.route("/detail/<course_id>", methods=["GET"])
def get_course_detail(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"success": False, "message": "Không tìm thấy khóa học"}), 404
    return jsonify({"success": True, "data": course})
