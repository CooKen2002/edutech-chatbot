# File location: backend/app/models/progress.py

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['edutech_chatbot']
progress_collection = db['progress']

# Hàm tạo bản ghi tiến độ mới
def create_progress(user_email, course_name, completion_percent=0):
    result = progress_collection.update_one(
        {"user_email": user_email, "course_name": course_name},
        {
            "$set": {
                "completion_percent": completion_percent,
                "last_updated": datetime.utcnow()
            }
        },
        upsert=True
    )
    return result.upserted_id or True


# Hàm lấy tiến độ theo user và course
def get_progress(user_email, course_name):
    return progress_collection.find_one({'user_email': user_email, 'course_name': course_name})

# Hàm cập nhật tiến độ học
def update_progress(user_email, course_name, completion_percent):
    update_data = {
        'completion_percent': completion_percent,
        'last_updated': datetime.utcnow()
    }
    return progress_collection.update_one(
        {'user_email': user_email, 'course_name': course_name},
        {'$set': update_data},
        upsert=True  # Nếu chưa có thì tạo mới
    )

# Hàm lấy tất cả tiến độ của 1 user
def get_all_progress_by_user(user_email):
    return list(progress_collection.find({'user_email': user_email}))
