import os
from pymongo import MongoClient

def create_test_users():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client.edutech_chatbot
    users_collection = db.users

    # Xóa tất cả người dùng hiện có trong collection
    users_collection.delete_many({})

    # Danh sách người dùng test
    users = [
        {
            "email": "user1@example.com",
            "password": "password123",
            "learning_progress": [{"course": "Math", "progress": 50}],
            "interests": ["math", "science"],
            "learning_path": "Basic Math -> Advanced Math",
            "hobby": "Reading",
            "subj": "Math",
            "progress_ids": []  # Thêm trường progress_ids (danh sách trống)
        },
        {
            "email": "user2@example.com",
            "password": "password123",
            "learning_progress": [{"course": "English", "progress": 70}],
            "interests": ["languages", "reading"],
            "learning_path": "Basic English -> Advanced English",
            "hobby": "Traveling",
            "subj": "English",
            "progress_ids": []  # Thêm trường progress_ids (danh sách trống)
        },
        {
            "email": "user3@example.com",
            "password": "password123",
            "learning_progress": [{"course": "Science", "progress": 40}],
            "interests": ["science", "technology"],
            "learning_path": "Basic Science -> Advanced Science",
            "hobby": "Gaming",
            "subj": "Science",
            "progress_ids": []  # Thêm trường progress_ids (danh sách trống)
        }
    ]

    # Chèn người dùng vào collection
    users_collection.insert_many(users)
    print("Created test users successfully.")

if __name__ == "__main__":
    create_test_users()
