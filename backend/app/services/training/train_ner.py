import os
import torch
import numpy as np
from torch.utils.data import DataLoader, random_split, Dataset
from transformers import AutoModelForTokenClassification, AutoTokenizer
from torch.optim import AdamW
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_ner_data(file_path):
    """Đọc file dữ liệu NER theo định dạng: word TAB tag, cách dòng bằng dòng trống"""
    sentences = []
    labels = []
    sentence = []
    label_seq = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    if sentence:
                        sentences.append(sentence)
                        labels.append(label_seq)
                        sentence = []
                        label_seq = []
                else:
                    parts = line.split("\t")
                    if len(parts) != 2:
                        raise ValueError(f"Lỗi định dạng dòng: {line}")
                    word, tag = parts
                    sentence.append(word)
                    label_seq.append(tag)

            # Thêm câu cuối nếu chưa thêm
            if sentence:
                sentences.append(sentence)
                labels.append(label_seq)
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu NER từ file {file_path}: {e}")
        raise e

    return sentences, labels


def encode_tags(tags, encodings, label2id):
    """
    Mã hóa nhãn cho từng token (cho fast tokenizer có word_ids())
    Trả về list list label ids
    """
    encoded_labels = []
    for i, doc_labels in enumerate(tags):
        word_ids = encodings.word_ids(batch_index=i)  # trả về index word tương ứng token
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # token padding hoặc special token không tính loss
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[doc_labels[word_idx]])
            else:
                label_ids.append(-100)  # các token con của 1 từ bỏ qua
            previous_word_idx = word_idx
        encoded_labels.append(label_ids)
    return encoded_labels


class NERDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])


def train_epoch(model, data_loader, optimizer, device):
    model.train()
    losses = []
    loop = tqdm(data_loader, desc="Training", leave=False)
    for batch in loop:
        optimizer.zero_grad()
        inputs = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        loop.set_postfix(loss=loss.item())
    return np.mean(losses)


def main():
    # Đường dẫn file dữ liệu train NER
    file_path = os.path.join(BASE_DIR, "train_ner.txt")
    print(f"Đang load dữ liệu từ: {file_path}")
    sentences, labels = load_ner_data(file_path)
    print(f"Tổng số câu: {len(sentences)}")

    label_list = ["O", "B-MONHOC", "I-MONHOC", "B-SOTHICH", "I-SOTHICH"]
    label2id = {label: i for i, label in enumerate(label_list)}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Sử dụng thiết bị: {device}")

    # Load tokenizer fast (cần cho word_ids())
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base", use_fast=True)

    # Mã hóa câu (sentence split into words)
    encodings = tokenizer(
        sentences,
        is_split_into_words=True,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors=None
    )

    # Mã hóa nhãn tương ứng
    encoded_labels = encode_tags(labels, encodings, label2id)
    encodings["labels"] = encoded_labels

    # Tạo dataset và chia train/val
    dataset = NERDataset(encodings)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16)

    # Khởi tạo model token classification với số nhãn phù hợp
    model = AutoModelForTokenClassification.from_pretrained(
        "xlm-roberta-base",
        num_labels=len(label_list)
    ).to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5)
    epochs = 4

    print("Bắt đầu huấn luyện NER model...")
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        train_loss = train_epoch(model, train_loader, optimizer, device)
        print(f"Loss trung bình epoch {epoch + 1}: {train_loss:.4f}")

    # Lưu mô hình và tokenizer
    save_dir = os.path.join(BASE_DIR, "models", "xlm_ner")
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Đã lưu mô hình và tokenizer vào: {save_dir}")

    print("Hoàn thành huấn luyện NER!")


if __name__ == "__main__":
    main()
