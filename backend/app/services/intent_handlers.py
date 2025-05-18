# File: backend/app/services/intent_handlers.py

from .learning_styles import generate_learning_styles
from .learning_path_service import generate_learning_path
from ..services.user_service import update_user_preferences, get_user_info
from ..models.user import update_user
from ..models.progress import create_progress

# Dùng biến tạm (hoặc có thể quản lý trạng thái chat nâng cao hơn ở DB)
chat_sessions = {}

def handle_learning_need(email, entities, user_input, session_id=None):
    session = chat_sessions.get(session_id, {"step": 1, "selected_course": None})

    if session["step"] == 1:
        return handle_step_1(session, entities, session_id)

    elif session["step"] == 2:
        return handle_step_2(session, user_input, session_id, email)

    elif session["step"] == 3:
        return handle_step_3(email, user_input, session_id)

    else:
        return "Cảm ơn bạn đã trao đổi. Nếu cần hỗ trợ thêm, bạn cứ hỏi nhé!"

def handle_step_1(session, entities, session_id):
    subjects = entities.get("MONHOC", [])
    if not subjects:
        return "Bạn muốn học về lĩnh vực gì? Vui lòng nhập tên môn học hoặc kỹ năng bạn muốn học."

    learning_path = generate_learning_path(subjects[0])
    if learning_path:
        session["step"] = 2
        session["learning_path"] = learning_path
        chat_sessions[session_id] = session

        response = f"Tôi tìm thấy {len(learning_path)} khóa học cho {subjects[0]}:\n"
        for idx, course in enumerate(learning_path[:5], 1):
            response += f"{idx}. {course['name']} ({course['difficulty']}, {course['duration']} giờ)\n"
        response += "\nBạn muốn chọn khóa học nào? Vui lòng nhập số tương ứng."
        return response

    return f"Xin lỗi, hiện tại tôi chưa tìm thấy khóa học phù hợp cho {subjects[0]}."

def handle_step_2(session, user_input, session_id, email):
    print("DEBUG: session in step 2:", session)  # Debug session

    try:
        choice = int(user_input.strip())
        learning_path = session.get("learning_path", [])
        if not learning_path:
            return "Lỗi: không tìm thấy danh sách khóa học để chọn. Bạn hãy bắt đầu lại nhé."

        if 1 <= choice <= len(learning_path):
            selected_course = learning_path[choice - 1]
            session["selected_course"] = selected_course
            session["step"] = 3
            chat_sessions[session_id] = session

            course_name = selected_course.get("name")

            # Lưu tiến độ mới hoặc tạo mới
            create_progress(email, course_name, completion_percent=0)

            # Cập nhật user: đổi trường thành selected_course cho rõ ràng
            update_result = update_user(email, {
                "selected_course": course_name,
            })
            print("DEBUG update_user result:", update_result)

            user = get_user_info(email)
            existing_hobbies = user.get("hobby", [])
            if isinstance(existing_hobbies, str):
                existing_hobbies = [existing_hobbies]

            if existing_hobbies:
                learning_styles = generate_learning_styles(existing_hobbies)
                return (
                    f"Bạn đã chọn khóa học: {course_name}.\n"
                    f"Bạn đã có sở thích: {', '.join(existing_hobbies)}.\n"
                    f"Phong cách học phù hợp với bạn: {', '.join(learning_styles)}.\n"
                    "Chúc bạn học tốt nhé!"
                )
            else:
                return (
                    f"Bạn đã chọn khóa học: {course_name}.\n"
                    "Bạn có sở thích cá nhân nào không? Hãy chia sẻ để tôi gợi ý phong cách học phù hợp."
                )

        return f"Số bạn chọn không hợp lệ. Vui lòng chọn số từ 1 đến {len(learning_path)}."

    except ValueError:
        return "Vui lòng nhập một số để chọn khóa học."

def handle_step_3(email, user_input, session_id):
    user = get_user_info(email)
    existing_hobbies = user.get("hobby", [])

    if existing_hobbies:
        # Nếu người dùng đã có sở thích, sử dụng luôn để gợi ý phong cách học
        learning_styles = generate_learning_styles(existing_hobbies)
        response = (
            f"Bạn đã có sở thích: {', '.join(existing_hobbies)}.\n"
            f"Phong cách học phù hợp với bạn: {', '.join(learning_styles)}.\n"
            "Chúc bạn học tốt nhé!"
        )
        chat_sessions.pop(session_id, None)
        return response

    # Nếu chưa có sở thích, hỏi người dùng nhập vào
    hobbies = [h.strip() for h in user_input.split(",") if h.strip()]
    if not hobbies:
        return "Bạn có thể chia sẻ sở thích của mình để tôi gợi ý phong cách học phù hợp."

    # Lưu sở thích mới vào hồ sơ
    update_user_preferences(email, {"SOTHICH": hobbies})
    learning_styles = generate_learning_styles(hobbies)

    response = (
        f"Cảm ơn bạn đã chia sẻ sở thích {', '.join(hobbies)}.\n"
        f"Phong cách học phù hợp với bạn: {', '.join(learning_styles)}.\n"
        "Chúc bạn học tốt nhé!"
    )

    chat_sessions.pop(session_id, None)
    return response

def handle_learning_path(entities):
    subjects = entities.get("MONHOC", [])
    if not subjects:
        return "Bạn muốn tìm hiểu lộ trình học môn nào? Hãy cho tôi biết thêm nhé."

    learning_path = generate_learning_path(subjects[0])
    if learning_path:
        response = f"Tôi tìm thấy {len(learning_path)} khóa học cho {subjects[0]}:\n"
        for course in learning_path[:5]:
            response += f"- {course['name']} ({course['difficulty']}, {course['duration']} giờ)\n"
        return response

    return f"Xin lỗi, hiện tại tôi chưa tìm thấy khóa học phù hợp cho {subjects[0]}."

def handle_study():
    return "Bạn muốn tôi chia sẻ cách học hiệu quả hoặc kỹ thuật nào?"

def handle_hobbies(email, entities):
    hobbies = entities.get("SOTHICH", [])
    if not hobbies:
        return "Bạn có thể chia sẻ sở thích của mình để tôi gợi ý lộ trình học phù hợp."

    # Lấy thông tin người dùng
    user = get_user_info(email)
    user_hobbies = set(user.get("hobby", []))  # Sử dụng set để tránh trùng lặp
    user_interests = set(user.get("interests", []))

    # Thêm sở thích vào danh sách hobby
    user_hobbies.update(hobbies)

    # Nếu sở thích là môn học, thêm vào interests
    known_subjects = {"toán", "văn", "anh", "lý", "hóa", "sinh", "lịch sử", "địa lý", "công nghệ", "tin học"}
    for hobby in hobbies:
        if hobby.lower() in known_subjects:
            user_interests.add(hobby)

    # Cập nhật sở thích và môn học trong database
    update_result = update_user(email, {
        "hobby": list(user_hobbies),
        "interests": list(user_interests)
    })
    if not update_result.get('success'):
        print(f"[WARN] Update user failed when updating hobbies: {update_result.get('message')}")

    # Gợi ý phong cách học dựa trên sở thích
    learning_styles = generate_learning_styles(list(user_hobbies))

    return (
        f"Cảm ơn bạn đã chia sẻ sở thích {', '.join(hobbies)}.\n"
        f"Phong cách học phù hợp với bạn: {', '.join(learning_styles)}."
    )

def handle_unknown():
    return "Tôi chưa hiểu ý bạn. Bạn có thể nói rõ hơn không?"
