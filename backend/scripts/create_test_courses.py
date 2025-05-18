# backend/app/database/init_courses_database.py

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['edutech_chatbot']
courses_collection = db['courses']

# Xóa các khóa học cũ nếu có
courses_collection.delete_many({})

courses = [
    # Python
    {'name': 'Python', 'description': 'Học các kiến thức cơ bản về lập trình Python.', 'category': 'python', 'difficulty': 'beginner', 'duration': 10, 'format': 'online', 'provider': 'Udemy'},
    {'name': 'Python', 'description': 'Nâng cao kỹ năng lập trình Python.', 'category': 'python', 'difficulty': 'advanced', 'duration': 20, 'format': 'online', 'provider': 'Coursera'},

    # Java
    {'name': 'Java', 'description': 'Bắt đầu học lập trình Java.', 'category': 'java', 'difficulty': 'beginner', 'duration': 12, 'format': 'online', 'provider': 'Udemy'},
    {'name': 'Java', 'description': 'Khám phá các chủ đề nâng cao trong Java.', 'category': 'java', 'difficulty': 'advanced', 'duration': 18, 'format': 'online', 'provider': 'Coursera'},

    # Toán
    {'name': 'Toán', 'description': 'Hiểu các khái niệm toán học cơ bản.', 'category': 'toán', 'difficulty': 'beginner', 'duration': 8, 'format': 'offline', 'provider': 'Trường địa phương'},
    {'name': 'Giải tích I', 'description': 'Giới thiệu về giải tích vi phân và tích phân.', 'category': 'toán', 'difficulty': 'intermediate', 'duration': 20, 'format': 'online', 'provider': 'Khan Academy'},
    {'name': 'Đại số tuyến tính', 'description': 'Lý thuyết ma trận và đại số tuyến tính.', 'category': 'toán', 'difficulty': 'advanced', 'duration': 25, 'format': 'online', 'provider': 'MIT OpenCourseWare'},

    # Vật lý
    {'name': 'Vật lý cơ bản', 'description': 'Học các kiến thức vật lý căn bản.', 'category': 'vật lý', 'difficulty': 'beginner', 'duration': 12, 'format': 'online', 'provider': 'Khan Academy'},
    {'name': 'Cơ học cổ điển', 'description': 'Nghiên cứu chuyên sâu về cơ học.', 'category': 'vật lý', 'difficulty': 'advanced', 'duration': 22, 'format': 'online', 'provider': 'edX'},

    # Hóa học
    {'name': 'Hóa học đại cương', 'description': 'Các khái niệm cơ bản trong hóa học.', 'category': 'hóa học', 'difficulty': 'beginner', 'duration': 10, 'format': 'offline', 'provider': 'Trường địa phương'},
    {'name': 'Hóa học hữu cơ', 'description': 'Nghiên cứu các phân tử hữu cơ.', 'category': 'hóa học', 'difficulty': 'advanced', 'duration': 18, 'format': 'online', 'provider': 'Coursera'},

    # Lịch sử
    {'name': 'Lịch sử thế giới', 'description': 'Tìm hiểu lịch sử thế giới.', 'category': 'lịch sử', 'difficulty': 'intermediate', 'duration': 20, 'format': 'online', 'provider': 'Coursera'},
    {'name': 'Lịch sử hiện đại', 'description': 'Học về các sự kiện lịch sử gần đây.', 'category': 'lịch sử', 'difficulty': 'advanced', 'duration': 15, 'format': 'online', 'provider': 'edX'},

    # Tiếng Anh
    {'name': 'Tiếng Anh cơ bản', 'description': 'Học các kỹ năng tiếng Anh cơ bản.', 'category': 'tiếng anh', 'difficulty': 'beginner', 'duration': 10, 'format': 'online', 'provider': 'Duolingo'},
    {'name': 'Ngữ pháp tiếng Anh nâng cao', 'description': 'Thành thạo ngữ pháp tiếng Anh.', 'category': 'tiếng anh', 'difficulty': 'advanced', 'duration': 15, 'format': 'online', 'provider': 'Udemy'},

    # Địa lý
    {'name': 'Địa lý tự nhiên', 'description': 'Nghiên cứu đặc điểm vật lý của Trái Đất.', 'category': 'địa lý', 'difficulty': 'intermediate', 'duration': 12, 'format': 'offline', 'provider': 'Trường địa phương'},

    # Kinh tế
    {'name': 'Nguyên lý kinh tế', 'description': 'Giới thiệu các nguyên lý kinh tế cơ bản.', 'category': 'kinh tế', 'difficulty': 'beginner', 'duration': 14, 'format': 'online', 'provider': 'Coursera'},

    # Marketing
    {'name': 'Marketing kỹ thuật số cơ bản', 'description': 'Học các nguyên lý cơ bản về marketing kỹ thuật số.', 'category': 'marketing', 'difficulty': 'beginner', 'duration': 10, 'format': 'online', 'provider': 'Udemy'},

    # Thiết kế
    {'name': 'Thiết kế đồ họa cơ bản', 'description': 'Kiến thức nền tảng về thiết kế đồ họa.', 'category': 'thiết kế', 'difficulty': 'beginner', 'duration': 12, 'format': 'online', 'provider': 'Coursera'},

    # Nhiếp ảnh
    {'name': 'Nhiếp ảnh cơ bản', 'description': 'Học cách chụp ảnh chuyên nghiệp.', 'category': 'nhiếp ảnh', 'difficulty': 'beginner', 'duration': 8, 'format': 'offline', 'provider': 'Local Studio'},

    # Lập trình Web
    {'name': 'Lập trình web toàn tập', 'description': 'Học phát triển web full-stack.', 'category': 'lập trình web', 'difficulty': 'beginner', 'duration': 25, 'format': 'online', 'provider': 'Udemy'},

    # Machine Learning
    {'name': 'Machine Learning cơ bản', 'description': 'Giới thiệu về học máy.', 'category': 'machine learning', 'difficulty': 'beginner', 'duration': 20, 'format': 'online', 'provider': 'Coursera'},
    {'name': 'Deep Learning nâng cao', 'description': 'Các kỹ thuật deep learning nâng cao.', 'category': 'machine learning', 'difficulty': 'advanced', 'duration': 30, 'format': 'online', 'provider': 'edX'},
]

courses_collection.insert_many(courses)

print("Khởi tạo database courses thành công với nhiều khóa học tiếng Việt có dấu.")
