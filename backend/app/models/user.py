# File location: backend/app/models/user.py

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['edutech_chatbot']
users_collection = db['users']

# Hàm tạo người dùng mới
def create_user(email, password, interests=None, hobby=None, subj=None):
    user = {
        'email': email,
        'password': password,
        'learning_progress': '',     
        'interests': interests if interests else [],
        'learning_path': '',
        'hobby': hobby,
        'subj': subj,
        'progress_ids': []  
    }

    users_collection.insert_one(user)
    return user

# Hàm lấy thông tin người dùng
def get_user_by_email(email):
    return users_collection.find_one({'email': email})

# Hàm cập nhật thông tin người dùng
def update_user(email, update_data):
    user = users_collection.find_one({'email': email})
    if not user:
        return {'success': False, 'message': 'User not found'}

    if 'interests' in update_data and isinstance(update_data['interests'], list):
        current_interests = set(user.get('interests', []))
        new_interests = set(update_data['interests'])
        update_data['interests'] = list(current_interests.union(new_interests))

    result = users_collection.update_one(
        {'email': email},
        {'$set': update_data},
        upsert=False
    )

    if result.modified_count > 0:
        return {'success': True, 'message': 'User updated successfully'}
    else:
        # Trường hợp dữ liệu đã giống dữ liệu cũ, nhưng bạn vẫn muốn coi là thành công
        return {'success': True, 'message': 'No fields were updated (data might be the same)'}
