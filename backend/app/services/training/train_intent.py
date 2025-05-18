# backend/app/services/ttraining/train_intent.py
import os
import torch
from torch.utils.data import DataLoader, random_split, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch.optim import AdamW
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, 'train_intent.csv')

class QuestionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoded = self.tokenizer(
            self.texts[idx],
            padding='max_length',
            truncation=True,
            max_length=128,
            return_tensors='pt'
        )
        return {
            'input_ids': encoded['input_ids'].squeeze(),
            'attention_mask': encoded['attention_mask'].squeeze(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

def train_epoch(model, data_loader, optimizer, device):
    model.train()
    losses = []
    all_preds = []
    all_labels = []

    for batch in tqdm(data_loader, desc="Training"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        logits = outputs.logits

        loss.backward()
        optimizer.step()

        losses.append(loss.item())
        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.detach().cpu().numpy())
        all_labels.extend(labels.detach().cpu().numpy())

    acc = accuracy_score(all_labels, all_preds)
    avg_loss = np.mean(losses)
    return avg_loss, acc

def eval_model(model, data_loader, device, label_encoder):
    model.eval()
    losses = []
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in tqdm(data_loader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            logits = outputs.logits

            losses.append(loss.item())
            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.detach().cpu().numpy())
            all_labels.extend(labels.detach().cpu().numpy())

    acc = accuracy_score(all_labels, all_preds)
    avg_loss = np.mean(losses)
    target_names = label_encoder.classes_
    labels = list(range(len(target_names)))
    report = classification_report(all_labels, all_preds, labels=labels, target_names=target_names)
    return avg_loss, acc, report

def main():
    print(f"Loading data from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    custom_labels = ['Nhu cầu học', 'Lộ trình học', 'Học tập', 'Sở thích']
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.array(custom_labels)
    labels_encoded = label_encoder.fit_transform(labels)

    print(f"Labels: {label_encoder.classes_}")

    tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base-v2')
    dataset = QuestionDataset(texts, labels_encoded, tokenizer)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = AutoModelForSequenceClassification.from_pretrained(
        'vinai/phobert-base-v2',
        num_labels=len(label_encoder.classes_)
    ).to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5)

    epochs = 4
    best_val_acc = 0

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device)
        print(f"Train loss: {train_loss:.4f}, Train accuracy: {train_acc:.4f}")

        val_loss, val_acc, val_report = eval_model(model, val_loader, device, label_encoder)
        print(f"Validation loss: {val_loss:.4f}, Validation accuracy: {val_acc:.4f}")
        print(f"Validation classification report:\n{val_report}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print("Saving best model and tokenizer...")
            save_dir = os.path.join(BASE_DIR, 'models', 'phobert_question_classifier')
            os.makedirs(save_dir, exist_ok=True)
            model.cpu()
            model.save_pretrained(save_dir)
            tokenizer.save_pretrained(save_dir)
            model.to(device)

    print("Training complete!")

if __name__ == "__main__":
    main()
