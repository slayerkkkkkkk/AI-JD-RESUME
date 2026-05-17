import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def signup(email, password):
    return requests.post(
        f"{BASE_URL}/auth/signup",
        json={"email": email, "password": password}
    )

def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )

def upload_resumes(files, company, visibility, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"company": company,
            "visibility": visibility}
    return requests.post(
        f"{BASE_URL}/resumes/upload",
        files=files,
        data=data,
        headers=headers
    )

def get_resumes(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/resumes/list", headers=headers)

def get_stats(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/resumes/stats", headers=headers)

def match_jd(jd_text, company, token):
    headers = {"Authorization": f"Bearer {token}"}
    #very important high risk change 
    payload = {
        "jd_text": jd_text,
        "company": company,
        "database_type": "private" if company else "public"
    }
    return requests.post(
        f"{BASE_URL}/jd/match",
        json=payload,
        headers=headers
    )

