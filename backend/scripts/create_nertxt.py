# File: scripts/create_nertxt.py

import random
import os

# Đường dẫn lưu file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "..", "app", "services", "training")
os.makedirs(save_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
file_path = os.path.join(save_dir, "train_ner.txt")

monhoc_list = [
    "toán học", "tiếng Anh", "lập trình Python", "vật lý", "hóa học",
    "khoa học máy tính", "thiết kế đồ họa", "phát triển phần mềm",
    "ngôn ngữ lập trình Java", "trí tuệ nhân tạo",
    "khoa học dữ liệu", "machine learning", "deep learning",
    "mạng máy tính", "phát triển web", "thiết kế UX/UI",
    "an ninh mạng", "hệ điều hành", "phân tích dữ liệu"
]

sothich_list = [
    "bóng đá", "đọc sách", "chơi guitar", "vẽ tranh", "đi du lịch",
    "chơi cờ vua", "chạy bộ", "đạp xe", "tập gym", "nghe nhạc",
    "nấu ăn", "làm bánh", "chụp ảnh", "leo núi",
    "xem phim", "mua sắm", "thể thao điện tử",
    "thử thách trí tuệ", "sáng tạo nội dung"
]

def create_ner_sentence(template, entity_list, entity_label):
    entity = random.choice(entity_list)
    sentence = template.replace("<ENTITY>", entity)

    words = sentence.split()
    entity_words = entity.split()

    labels = []
    i = 0
    while i < len(words):
        match = True
        for j in range(len(entity_words)):
            if i + j >= len(words) or words[i + j].lower() != entity_words[j].lower():
                match = False
                break
        if match:
            labels.append(f"B-{entity_label}")
            for k in range(1, len(entity_words)):
                labels.append(f"I-{entity_label}")
            i += len(entity_words)
        else:
            labels.append("O")
            i += 1

    return list(zip(words, labels))

def generate_data(num_samples=10000):
    templates = [
        "Tôi muốn học <ENTITY> .",
        "Bạn có thích <ENTITY> không ?",
        "Khóa học <ENTITY> bắt đầu vào tuần tới .",
        "Tôi thích chơi <ENTITY> .",
        "Sở thích của tôi là <ENTITY> .",
        "Em muốn tham gia khóa học <ENTITY> .",
        "Mình muốn trở thành chuyên gia về <ENTITY> .",
        "Cách tốt nhất để học <ENTITY> là gì ?",
        "Mình đam mê <ENTITY> và muốn tìm hiểu thêm .",
        "Hãy giới thiệu khóa học <ENTITY> cho tôi .",
        "Tôi muốn đăng ký lớp học <ENTITY> .",
        "Tại sao <ENTITY> lại quan trọng ?",
        "Tôi nên bắt đầu học <ENTITY> như thế nào ?",
        "Làm sao để cải thiện kỹ năng <ENTITY> ?",
        "Mình muốn biết kiến thức cơ bản về <ENTITY> ."
    ]

    data = []
    for _ in range(num_samples // 2):
        data.append(create_ner_sentence(random.choice(templates), monhoc_list, "MONHOC"))
        data.append(create_ner_sentence(random.choice(templates), sothich_list, "SOTHICH"))

    return data

def save_to_file(data):
    with open(file_path, "w", encoding="utf-8") as f:
        for sentence in data:
            for word, label in sentence:
                f.write(f"{word}\t{label}\n")
            f.write("\n")  # Cách câu bằng dòng trống

if __name__ == "__main__":
    ner_data = generate_data(10000)  # Số lượng câu là 10,000
    save_to_file(ner_data)
    print(f"Đã tạo file train_ner.txt với {len(ner_data)} câu tại: {file_path}")
