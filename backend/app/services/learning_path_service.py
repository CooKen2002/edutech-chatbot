from pymongo import MongoClient
import unidecode
from rapidfuzz import fuzz

client = MongoClient('mongodb://localhost:27017/')
db = client['edutech_chatbot']
courses_collection = db['courses']

def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = unidecode.unidecode(text)
    return text

def generate_learning_path(subject: str):

    if not subject:
        return []

    norm_subject = normalize_text(subject)
    all_courses = list(courses_collection.find())

    matched_courses = []
    threshold = 80  # ngưỡng fuzzy matching

    for course in all_courses:
        course_category = course.get('category', '')
        norm_category = normalize_text(course_category)
        score = fuzz.ratio(norm_subject, norm_category)
        if score >= threshold:
            matched_courses.append({
                "name": course.get('name'),
                "description": course.get('description'),
                "difficulty": course.get('difficulty'),
                "duration": course.get('duration'),
                "format": course.get('format'),
                "provider": course.get('provider'),
            })

    return matched_courses
