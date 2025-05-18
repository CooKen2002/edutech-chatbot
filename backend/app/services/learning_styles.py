def generate_learning_styles(hobbies):
    # Mapping từ sở thích sang phong cách học
    hobby_to_style = {
        "đọc sách": "Học qua đọc hiểu và nghiên cứu tài liệu",
        "nghe nhạc": "Học qua nghe và ghi âm",
        "thể thao": "Học qua thực hành và trải nghiệm",
        "công nghệ": "Học qua tương tác và thực hành trên máy tính",
        "vẽ": "Học qua hình ảnh và sáng tạo",
        "nấu ăn": "Học qua thực hành và làm thử",
        "xem phim": "Học qua nghe nhìn và phân tích",
        "chơi game": "Học qua tương tác và giải quyết vấn đề",
        "viết lách": "Học qua viết và phản hồi",
        "du lịch": "Học qua khám phá và trải nghiệm thực tế",
        "âm nhạc": "Học qua nghe và ghi nhớ âm thanh",
        "đi bộ": "Học qua vận động và trải nghiệm ngoài trời",
        "nhiếp ảnh": "Học qua quan sát và hình ảnh"
    }

    learning_styles = set()  # Sử dụng set để loại bỏ trùng lặp

    for hobby in hobbies:
        hobby_lower = hobby.lower()
        # Phân tích từng từ trong sở thích
        for key in hobby_to_style:
            if key in hobby_lower:
                learning_styles.add(hobby_to_style[key])

    # Nếu không tìm thấy phong cách nào, thêm phong cách mặc định
    if not learning_styles:
        learning_styles.add("Học theo phong cách chung: đọc, nghe, thực hành")

    return list(learning_styles)
