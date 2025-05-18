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
        "Tôi muốn biết về <ENTITY>"
    ],
    "Lộ trình học": [
        "Lộ trình học <ENTITY> như thế nào?",
        "Tôi cần lộ trình học <ENTITY>",
        "Lộ trình học phù hợp cho <ENTITY> là gì?"
    ],
    "Sở thích": [
        "Tôi thích <ENTITY>",
        "Sở thích của tôi là <ENTITY>",
        "Mình thích <ENTITY>"
    ],
    "Học tập": [
        "Cách học tập hiệu quả là gì?",
        "Làm sao để học tốt hơn?",
        "Mình muốn cải thiện kết quả học tập"
    ]
}

entities = [
    "tiếng Anh", "Python", "Java", "vật lý", "hóa học",
    "lập trình", "thiết kế đồ họa", "khoa học máy tính",
    "bóng đá", "đọc sách", "chơi guitar", "vẽ tranh"
]

def generate_intent_data(num_samples=500):
    data = []

    for _ in range(num_samples):
        intent = random.choice(list(intent_templates.keys()))
        template = random.choice(intent_templates[intent])

        if "<ENTITY>" in template:
            entity = random.choice(entities)
            text = template.replace("<ENTITY>", entity)
        else:
            text = template

        data.append([text, intent])

    return data

def save_to_csv(data):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(data)

if __name__ == "__main__":
    intent_data = generate_intent_data(1000)  # Số lượng câu tùy chọn
    save_to_csv(intent_data)
    print(f"Đã tạo file train_intent.csv với {len(intent_data)} câu tại: {file_path}")
