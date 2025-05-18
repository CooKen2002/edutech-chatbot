# EduuTech Chatbot Backend

## 🚀 Project Overview

This is the backend service for the EdTech Chatbot — an intelligent learning assistant that provides personalized learning paths, manages user profiles, and analyzes user queries with NLP models.

Built with **Flask**, connected to **MongoDB** for data storage, and incorporates **NLP model training** for smart question classification.

## 🛠️ Features

- RESTful API endpoints for courses, users, authentication, and learning progress
- MongoDB integration via PyMongo and MongoEngine
- JWT-based authentication and authorization
- NLP model training and inference (using Transformer-based models like PhoBERT)
- User profile and course progress management

## 📦 Requirements

- Python 3.9 or higher
- MongoDB server (local or remote)
- See [`requirements.txt`](./requirements.txt) for full Python dependencies

## ⚙️ Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://your-repo-url.git
   cd your-repo/backend

2. **Create and activate a Python virtual environment:**

    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. **Install dependencies:**

    pip install -r requirements.txt

4. **Create a .env file in the backend root folder:**

    MONGO_URI=mongodb://localhost:27017/edtechdb
    JWT_SECRET_KEY=your_secret_key_here
    FLASK_ENV=development

5. **Ensure MongoDB is running on your machine or accessible remotely.**

## ▶️ Running the Server

    python app.py

## 🧠 Model Training
This backend includes NLP training pipelines for classifying user queries:

    1. Locate backend/app/services/training/ directory.
    2. Train models using: 

        python train_intent.py
        python train_ner.py

    3. Models are saved in the models/ folder.
Note: 2 models above training throw 2 datafiles : **train_intent.csv and train_ner.txt**. You can generate with 2 script located in backend/scripts/ directory

## 🔗 API Endpoints

    | Method | Endpoint                        | Description                           |
    | ------ | ------------------------------- | ------------------------------------- |
    | GET    | `/api/course/detail/<courseId>` | Retrieve details of a course          |
    | GET    | `/api/user/profile`             | Get user profile information          |
    | POST   | `/api/user/profile`             | Update user profile                   |
    | POST   | `/api/auth/login`               | User login                            |
    | POST   | `/api/auth/register`            | User registration                     |
    | POST   | `/api/question/analyze`         | Analyze user questions with NLP model |

## 📋 Deployment on Another Machine
    Clone repo & setup Python environment.

    Install dependencies via requirements.txt.

    Setup .env file with correct environment variables.

    Ensure MongoDB service is accessible.

    Run the Flask app as described above.

## ❓ Troubleshooting & Notes

If you encounter connection issues, check MongoDB URI and service status.

Ensure all Python dependencies match versions in requirements.txt.

For large NLP models, GPU with CUDA is recommended for faster training.

## Happy coding and learning! 🎉