# backend/utils/bot.py

def process_user_message(message):
    """
    Xử lý tin nhắn từ người dùng và trả về phản hồi của chatbot.
    (Tạm thời dùng phản hồi đơn giản để test.)

    Args:
        message (str): Tin nhắn từ người dùng

    Returns:
        str: Phản hồi từ chatbot
    """
    message = message.lower()

    if "hello" in message or "hi" in message:
        return "Chào bạn! Tôi là chatbot học tập. Bạn muốn học gì hôm nay?"
    elif "math" in message:
        return "Bạn muốn học Toán cấp độ nào? Tiểu học, THCS hay THPT?"
    elif "bye" in message:
        return "Tạm biệt nhé! Chúc bạn học tốt."
    else:
        return "Tôi chưa hiểu rõ ý bạn. Bạn có thể nói rõ hơn không?"
