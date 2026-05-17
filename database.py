from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

raw_resumes = db.raw_resumes
processed_resumes = db.processed_resumes
recruiters_collection = db.recruiters


def ensure_indexes():
    try:
        raw_resumes.create_index("resume_id", unique=True)
        raw_resumes.create_index("visibility")
        raw_resumes.create_index("recruiter_id")
        processed_resumes.create_index("resume_id", unique=True)
        processed_resumes.create_index("visibility")
        processed_resumes.create_index("recruiter_id")
        recruiters_collection.create_index("email", unique=True)
    except Exception as e:
        print(f"Warning: Could not create indexes: {e}")
