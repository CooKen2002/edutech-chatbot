from ..extensions import mongo

def get_user_info(email):
    print(f"[DEBUG] get_user_info với email: {email}")
    if not mongo.cx:
        raise Exception("MongoDB chưa được khởi tạo.")
    user = mongo.db.users.find_one({"email": email})
    print(f"[DEBUG] Kết quả tìm user: {user}")
    return user if user else None

def update_user_info(email, data):
    if not mongo.cx:
        raise Exception("MongoDB chưa được khởi tạo.")
    print(f"[DEBUG] update_user_info với email: {email}, data: {data}")
    result = mongo.db.users.update_one({"email": email}, {"$set": data})
    print(f"[DEBUG] Modified count: {result.modified_count}")
    return result.modified_count > 0

def update_user_preferences(email, preferences):
    """
    Cập nhật từng trường con trong trường 'preferences' của user theo email.
    preferences là dict chứa các key-value sẽ được cập nhật.

    Ví dụ:
      preferences = {
          "favorite_subject": "toán",
          "learning_styles": ["Visual", "Kinesthetic"]
      }
    """
    if not mongo.cx:
        raise Exception("MongoDB chưa được khởi tạo.")
    
    print(f"[DEBUG] update_user_preferences với email: {email}, preferences: {preferences}")

    # Tạo dict với key dạng "preferences.<field>" để update nested field
    update_fields = {f"preferences.{key}": value for key, value in preferences.items()}

    result = mongo.db.users.update_one(
        {"email": email},
        {"$set": update_fields}
    )

    print(f"[DEBUG] Modified count: {result.modified_count}")
    return result.modified_count > 0