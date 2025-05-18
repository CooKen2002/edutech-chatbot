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
    "ngôn ngữ lập trình Java", "trí tuệ nhân tạo"
]

sothich_list = [
    "bóng đá", "đọc sách", "chơi guitar", "vẽ tranh", "đi du lịch",
    "chơi cờ vua", "chạy bộ", "đạp xe", "tập gym", "nghe nhạc"
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

def generate_data(num_samples=100):
    templates = [
        "Tôi muốn học <ENTITY> .",
        "Bạn có thích <ENTITY> không ?",
        "Khóa học <ENTITY> bắt đầu vào tuần tới .",
        "Tôi thích chơi <ENTITY> .",
        "Sở thích của tôi là <ENTITY> .",
        "Em muốn tham gia khóa học <ENTITY> ."
    ]

    data = []
    for _ in range(num_samples):
        # Lấy môn học
        template = random.choice(templates[:3])
        sent_label = create_ner_sentence(template, monhoc_list, "MONHOC")
        data.append(sent_label)

        # Lấy sở thích
        template = random.choice(templates[3:])
        sent_label = create_ner_sentence(template, sothich_list, "SOTHICH")
        data.append(sent_label)

    return data

def save_to_file(data):
    with open(file_path, "w", encoding="utf-8") as f:
        for sentence in data:
            for word, label in sentence:
                f.write(f"{word}\t{label}\n")
            f.write("\n")  # Cách câu bằng dòng trống

if __name__ == "__main__":
    ner_data = generate_data(500)  # Số lượng câu tùy chọn
    save_to_file(ner_data)
    print(f"Đã tạo file train_ner.txt với {len(ner_data)} câu tại: {file_path}")
