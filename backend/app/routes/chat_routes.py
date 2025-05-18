# File: backend/app/routes/chat_routes.py

from flask import Blueprint, request, jsonify
from ..services.user_service import get_user_info, update_user_preferences, update_user_info
from ..services.learning_styles import generate_learning_styles
from ..services.learning_path_service import generate_learning_path
from ..services.nlp_service import NLPModel
from ..services.intent_handlers import (
    handle_learning_need, handle_learning_path , handle_study, handle_hobbies, handle_unknown
)
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

nlp_model = NLPModel(
    intent_model_path="D:/Ken/Coding/edutech-chatbot/backend/app/services/training/models/phobert_question_classifier",
    entity_model_path="D:/Ken/Coding/edutech-chatbot/backend/app/services/training/models/xlm_ner"
)

SUBJECT_KEYWORDS = ["python", "java", "toán", "vật lý", "hóa học", "địa lý", "lịch sử", "tiếng anh"]


def extract_hobbies_from_message(message):
    lowered = message.lower()
    for prefix in ["tôi thích ", "sở thích của tôi là ", "mình thích "]:
        if lowered.startswith(prefix):
            hobbies_text = message[len(prefix):].strip()
            return [h.strip() for h in hobbies_text.replace(" và ", ",").split(",") if h.strip()]
    return [message.strip()]


def process_nlp(user_message):
    try:
        nlp_result = nlp_model.predict(user_message)
        print(f"[DEBUG] NLP raw output: {nlp_result}")
        intent = nlp_result.get("intent", "Không xác định")
        confidence = nlp_result.get("intent_confidence", 0)
        entities = nlp_result.get("entities", {})
    except Exception as e:
        print(f"Error in NLP Model: {str(e)}")
        return "Không xác định", 0, {}
    
    print(f"[DEBUG] Intent before fixup: {intent}, Entities before fixup: {entities}")
    
    if intent == "Lộ trình học" and not entities.get("MONHOC"):
        found_subjects = [kw for kw in SUBJECT_KEYWORDS if kw in user_message.lower()]
        if found_subjects:
            entities["MONHOC"] = found_subjects

    print(f"[DEBUG] Intent after fixup: {intent}, Entities after fixup: {entities}")
        
    return intent, confidence, entities


@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    email = data.get("email", "").strip()

    print(f"[DEBUG] Incoming message: {user_message}, Email: {email}")

    if not user_message:
        return jsonify({"response": "Vui lòng nhập nội dung."}), 400
    if not email:
        return jsonify({"response": "Email không được để trống."}), 400

    user = get_user_info(email)
    if not user:
        return jsonify({"response": "Email chưa đăng ký hoặc không tìm thấy người dùng."}), 404

    conversation_state = user.get("conversation_state", "")

    if conversation_state == "waiting_for_hobbies":
        hobbies = extract_hobbies_from_message(user_message)
        if hobbies:
            update_user_preferences(email, {"sothich": hobbies})
            update_user_info(email, {"conversation_state": ""})

            learning_styles = generate_learning_styles(hobbies)
            return jsonify({"response": f"Cảm ơn bạn đã chia sẻ sở thích: {', '.join(hobbies)}.\nPhong cách học phù hợp với bạn gồm: {', '.join(learning_styles)}."}), 200

        return jsonify({"response": "Xin lỗi, tôi chưa nhận được sở thích từ bạn. Bạn có thể nói lại không?"}), 200

    intent, confidence, entities = process_nlp(user_message)

    print(f"[DEBUG] Intent: {intent}, Confidence: {confidence}, Entities: {entities}")
    
    if confidence < 0.11:
        return jsonify({"response": "Xin lỗi, tôi chưa hiểu ý bạn. Bạn có thể nói rõ hơn không?"}), 200

    if intent == "Nhu cầu học" or intent == "Học tập":
        response = handle_learning_need(email, entities, user_message, session_id=email)
    elif intent == "Lộ trình học":
        response = handle_learning_path(entities)
    # elif intent == "Học tập":
        # response = handle_study()
    elif intent == "Sở thích":
        response = handle_hobbies(email, entities)
    else:
        response = handle_unknown()

    return jsonify({"response": response}), 200
