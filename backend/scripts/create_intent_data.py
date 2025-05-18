# File: scripts/create_intent_data.py

import random
import os
import csv

# Đường dẫn lưu file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "..", "app", "services", "training")
os.makedirs(save_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
file_path = os.path.join(save_dir, "train_intent.csv")

intent_templates = {
    "Nhu cầu học": [
        "Tôi muốn học <ENTITY>",
        "Tôi cần học <ENTITY>",
        "Tôi muốn biết về <ENTITY>",
        "Làm sao để học <ENTITY> nhanh nhất?",
        "Mình muốn bắt đầu học <ENTITY>"
    ],
    "Lộ trình học": [
        "Lộ trình học <ENTITY> như thế nào?",
        "Tôi cần lộ trình học <ENTITY>",
        "Lộ trình học phù hợp cho <ENTITY> là gì?",
        "Tôi muốn tìm hiểu lộ trình cho <ENTITY>",
        "Lộ trình học từ cơ bản đến nâng cao của <ENTITY>"
    ],
    "Sở thích": [
        "Tôi thích <ENTITY>",
        "Sở thích của tôi là <ENTITY>",
        "Mình thích <ENTITY>",
        "Mình đam mê <ENTITY>",
        "<ENTITY> là niềm yêu thích của mình"
    ],
    "Học tập": [
        "Cách học tập hiệu quả là gì?",
        "Làm sao để học tốt hơn?",
        "Mình muốn cải thiện kết quả học tập",
        "Phương pháp học <ENTITY> hiệu quả?",
        "Cách nhớ lâu khi học <ENTITY>"
    ],
    "Đánh giá kỹ năng": [
        "Tôi giỏi <ENTITY> không?",
        "Làm sao để biết trình độ <ENTITY> của mình?",
        "Mình muốn đánh giá kỹ năng <ENTITY>"
    ],
    "Đề xuất khóa học": [
        "Khóa học nào tốt nhất về <ENTITY>?",
        "Tôi nên học khóa nào về <ENTITY>?",
        "Khóa học <ENTITY> nào phù hợp với người mới bắt đầu?"
    ]
}

entities = [
    "tiếng Anh", "Python", "Java", "vật lý", "hóa học",
    "lập trình", "thiết kế đồ họa", "khoa học máy tính",
    "bóng đá", "đọc sách", "chơi guitar", "vẽ tranh",
    "nấu ăn", "marketing", "data science", "AI",
    "thiết kế web", "phát triển ứng dụng", "chỉnh sửa video",
    "sáng tạo nội dung", "SEO", "mạng xã hội",
    "sinh học", "toán học", "điện tử", "robotics",
    "viết lách", "thương mại điện tử", "blockchain",
    "an ninh mạng", "quản lý thời gian", "tư duy phản biện"
]

def generate_intent_data(num_samples=10000):
    data = [
        [random.choice(intent_templates[intent]).replace("<ENTITY>", random.choice(entities)), intent]
        for intent in random.choices(list(intent_templates.keys()), k=num_samples)
    ]
    return data

def save_to_csv(data):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(data)

if __name__ == "__main__":
    intent_data = generate_intent_data(10000)  # Số lượng câu là 10,000
    save_to_csv(intent_data)
    print(f"Đã tạo file train_intent.csv với {len(intent_data)} câu tại: {file_path}")
