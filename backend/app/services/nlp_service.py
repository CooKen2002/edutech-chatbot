import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
from pathlib import Path
import torch
import nltk

# Tải punkt nếu chưa có
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

class NLPModelIntent:
    def __init__(self, model_path="training/models/phobert_question_classifier"):
        try:
            base_path = Path(__file__).resolve().parent
            self.model_path = base_path / model_path
            model_path_str = self.model_path.as_posix()  # CHỈNH SỬA
            print(f"[Intent Model] Loading model from: {model_path_str}")

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path_str,
                use_fast=False,
                local_files_only=True
            )
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_path_str,
                local_files_only=True
            ).to(self.device)

        except Exception as e:
            raise RuntimeError(f"Lỗi khi tải mô hình intent classification: {str(e)}")

        self.model.eval()
        self.label_names = ["Nhu cầu học", "Lộ trình học", "Học tập", "Sở thích"]

    def preprocess(self, text):
        if not text or not text.strip():
            raise ValueError("Văn bản nhập vào không được rỗng.")
        return text.strip().lower()

    def predict(self, text):
        text = self.preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(self.device)
        with torch.no_grad():
            logits = self.model(**encoded_input).logits
        conf, pred_idx = torch.softmax(logits, dim=1).max(dim=1)
        return {"text": text, "label": self.label_names[pred_idx.item()], "confidence": conf.item()}


class NLPModelEntity:
    def __init__(self, model_path="training/models/xlm_ner"):
        try:
            base_path = Path(__file__).resolve().parent
            self.model_path = base_path / model_path
            model_path_str = self.model_path.as_posix()  # CHỈNH SỬA
            print(f"[Entity Model] Loading model from: {model_path_str}")

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path_str,
                use_fast=False,
                local_files_only=True
            )
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = AutoModelForTokenClassification.from_pretrained(
                model_path_str,
                local_files_only=True
            ).to(self.device)

        except Exception as e:
            raise RuntimeError(f"Lỗi khi tải mô hình entity extraction: {str(e)}")
        
        self.model.eval()
        self.labels = ["O", "B-MONHOC", "I-MONHOC", "B-SOTHICH", "I-SOTHICH"]

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(self.device)
        with torch.no_grad():
            predictions = torch.argmax(self.model(**inputs).logits, dim=2)

        tokens = self.tokenizer.tokenize(text)
        # Bỏ token [CLS], [SEP] (thường là đầu/cuối)
        pred_labels = predictions[0].cpu().numpy()[1:len(tokens)+1]
        return [(token, self.labels[pred]) for token, pred in zip(tokens, pred_labels)]

    def extract_entities(self, token_label_pairs):
        entities = {"MONHOC": [], "SOTHICH": []}
        current_entity, current_label = [], None

        for token, label in token_label_pairs:
            if label == "O" and current_entity:
                entities[current_label].append(self._clean_entity_tokens(current_entity))
                current_entity = []
                current_label = None
            elif label.startswith("B-"):
                if current_entity:
                    entities[current_label].append(self._clean_entity_tokens(current_entity))
                current_entity = [token]
                current_label = label[2:]
            elif label.startswith("I-") and current_label == label[2:]:
                current_entity.append(token)

        if current_entity:
            entities[current_label].append(self._clean_entity_tokens(current_entity))

        return entities

    def _clean_entity_tokens(self, tokens):
        return " ".join(token.replace("▁", "") for token in tokens)


class NLPModel:
    def __init__(self, intent_model_path=None, entity_model_path=None):
        self.intent_model = NLPModelIntent(intent_model_path) if intent_model_path else None
        self.entity_model = NLPModelEntity(entity_model_path) if entity_model_path else None

    def predict_intent(self, text):
        if self.intent_model:
            return self.intent_model.predict(text)
        else:
            return {"error": "Mô hình intent chưa được khởi tạo."}

    def extract_entities(self, text):
        if self.entity_model:
            token_label_pairs = self.entity_model.predict(text)
            return self.entity_model.extract_entities(token_label_pairs)
        else:
            return {"error": "Mô hình entity chưa được khởi tạo."}

    def predict(self, text):
        intent_result = self.predict_intent(text)
        if "error" in intent_result:
            return intent_result
        entities = self.extract_entities(text)
        return {
            "text": text,
            "intent": intent_result["label"],
            "intent_confidence": intent_result["confidence"],
            "entities": entities
        }


if __name__ == "__main__":
    try:
        nlp_model = NLPModel(
            intent_model_path="training/models/phobert_question_classifier",
            entity_model_path="training/models/xlm_ner"
        )
        test_text = "Tôi muốn biết về Java"
        result = nlp_model.predict(test_text)
        print("Kết quả phân loại và trích xuất:", result)
    except Exception as e:
        print(f"Lỗi khi khởi tạo mô hình: {str(e)}")
