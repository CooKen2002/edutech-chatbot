# test_mongo.py
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Kiểm tra kết nối bằng cách truy vấn cơ sở dữ liệu
try:
    db = client["edutech_chatbot"]  # Sử dụng tên cơ sở dữ liệu của bạn
    print("Kết nối MongoDB thành công!")
    print(f"Các collections có sẵn: {db.list_collection_names()}")
except Exception as e:
    print(f"Lỗi kết nối MongoDB: {e}")
