# File location: backend/app/models/course.py
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['edutech_chatbot']
courses_collection = db['courses']

# Hàm tạo khóa học mới
def create_course(name, description, category, difficulty, duration, format, provider):
    course = {
        'name': name,
        'description': description,
        'category': category,
        'difficulty': difficulty,
        'duration': duration,
        'format': format,
        'provider': provider
    }
    courses_collection.insert_one(course)
    return course

# Hàm lấy tất cả khóa học
def get_all_courses():
    return list(courses_collection.find())

# Hàm lấy khóa học theo danh mục
def get_courses_by_category(category):
    return list(courses_collection.find({'category': category}))

def get_course_by_id(course_id):
    try:
        course = courses_collection.find_one({"_id": ObjectId(course_id)})
        if course:
            course["_id"] = str(course["_id"])  # Chuyển ObjectId thành string
        return course
    except Exception:
        return None