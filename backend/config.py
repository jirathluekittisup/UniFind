import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_EXPIRY_HOURS = 24 * 7

    MYSQL = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "user": os.getenv("MYSQL_USER", "unifind"),
        "password": os.getenv("MYSQL_PASSWORD", "unifind_pass"),
        "database": os.getenv("MYSQL_DB", "unifind"),
    }

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "unifind")

    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "./firebase-service-account.json")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")

    ALLOWED_EMAIL_DOMAIN = os.getenv("ALLOWED_EMAIL_DOMAIN", "student.chula.ac.th")

    PORT = int(os.getenv("FLASK_PORT", 5001))

    CATEGORIES = [
        "Electronics", "Accessories", "Clothing", "Documents",
        "Keys", "Bags", "Books", "Other",
    ]
