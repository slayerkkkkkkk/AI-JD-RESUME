import os
import shutil
import uuid
from datetime import datetime, timedelta
from fastapi import UploadFile
from chroma_client import get_collection
from database import raw_resumes, processed_resumes
from embedding import generate_embedding
from llm_parser import parse_resume
from utils import extract_text, clean_text

RAW_DIR = "data/raw_resumes"
PROCESSED_DIR = "data/processed_resumes"

# ======================= HELPERS =======================

def clean_metadata(metadata: dict) -> dict:
    """
    Remove None values from metadata.
    ChromaDB does NOT allow nulls.
    """
    return {k: v for k, v in metadata.items() if v is not None}

def upload_resumes_service(
    files,
    visibility: str,
    company: str | None,
    recruiter_id: str | None
):
    """
    Upload resumes into the same raw & processed collections.
    Visibility determines whether resume is public or private.
    """

    if visibility not in {"public", "private"}:
        raise ValueError("visibility must be 'public' or 'private'")

    if visibility == "private" and not company:
        raise ValueError("Private resumes require a company name")

    results = []

    # vector DB collection
    chroma_collection = get_collection("resumes")
    print("all files",files)
    for file in files:
        print(file)
        resume_id =str(uuid.uuid4())

        raw_path = os.path.join(RAW_DIR, f"{resume_id}_{file.filename}")
        processed_path = os.path.join(PROCESSED_DIR, f"{resume_id}_{file.filename}")

        # ------------------ SAVE RAW FILE ------------------
        with open(raw_path, "wb") as f:
            f.write(file.file.read())

        raw_text = extract_text(raw_path)
        cleaned_text = clean_text(raw_text)

        # ------------------ RAW DB INSERT ------------------
        raw_resumes.insert_one({
            "resume_id": resume_id,
            "raw_text": raw_text,
            "visibility": visibility,
            "company": company if visibility == "private" else None,
            "recruiter_id": recruiter_id if visibility == "private" else None,
            "uploaded_at": datetime.utcnow()
        })

        # ------------------ PROCESS ------------------
        structured_data = parse_resume(cleaned_text)
        embedding = generate_embedding(cleaned_text)

        # ------------------ VECTOR STORE ------------------
        metadata = clean_metadata({
            "resume_id": resume_id,
            "visibility": visibility,
            "company": company if visibility == "private" else None
        })

        chroma_collection.add(
            ids=[resume_id],
            embeddings=[embedding],
            # metadatas=[metadata]
            #very risky high risk change
            metadatas=[{
        "resume_id": resume_id,
        "visibility": visibility,   # public/private
        "company": company if visibility == "private" else ""
    }]
        )

        # ------------------ MOVE FILE ------------------
        shutil.move(raw_path, processed_path)

        # ------------------ PROCESSED DB INSERT ------------------
        processed_resumes.insert_one({
            "resume_id": resume_id,
            "structured": structured_data,
            "visibility": visibility,
            "company": company if visibility == "private" else None,
            "recruiter_id": recruiter_id if visibility == "private" else None,
            "uploaded_at": datetime.utcnow(),
            "auto_public_at": (
                datetime.utcnow() + timedelta(days=7)
                if visibility == "private"
                else None
            )
        })

        results.append({
            "resume_id": resume_id,
            "name": structured_data.get("name"),
            "visibility": visibility
        })

    return results

# ======================= UPDATE =======================

def update_resume_service(
    resume_id: str,
    file: UploadFile,
    recruiter_id: str
):
    resume = processed_resumes.find_one({"resume_id": resume_id})
    if not resume:
        raise ValueError("Resume not found")

    if resume["recruiter_id"] != recruiter_id:
        raise ValueError("Unauthorized")

    collection_name = (
        "public_resumes"
        if resume["visibility"] == "public"
        else f"private_{resume['company']}"
    )
    collection = get_collection(collection_name)

    # Delete old embedding
    collection.delete(ids=[resume_id])

    # Save new raw file
    filename = f"{resume_id}_{file.filename}"
    raw_path = os.path.join(RAW_DIR, filename)
    processed_path = os.path.join(PROCESSED_DIR, filename)

    with open(raw_path, "wb") as f:
        f.write(file.file.read())

    # Reprocess
    raw_text = extract_text(raw_path)
    cleaned_text = clean_text(raw_text)
    structured_data = parse_resume(cleaned_text)
    embedding = generate_embedding(cleaned_text)

    # Add updated embedding
    metadata = clean_metadata({
        "resume_id": resume_id,
        "visibility": resume["visibility"],
        "company": resume.get("company"),
        "recruiter_id": recruiter_id
    })

    collection.add(
        ids=[resume_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )

    shutil.move(raw_path, processed_path)

    processed_resumes.update_one(
        {"resume_id": resume_id},
        {"$set": {
            "structured": structured_data,
            "updated_at": datetime.utcnow()
        }}
    )

    return {"message": "Resume updated successfully"}


# ======================= DELETE =======================

def delete_resume_service(
    resume_id: str,
    recruiter_id: str
):
    resume = processed_resumes.find_one({"resume_id": resume_id})
    if not resume:
        raise ValueError("Resume not found")

    if resume["recruiter_id"] != recruiter_id:
        raise ValueError("Unauthorized")

    collection_name = (
        "public_resumes"
        if resume["visibility"] == "public"
        else f"private_{resume['company']}"
    )
    collection = get_collection(collection_name)

    # Delete embedding
    collection.delete(ids=[resume_id])

    # Delete MongoDB record
    processed_resumes.delete_one({"resume_id": resume_id})

    # Delete file
    for f in os.listdir(PROCESSED_DIR):
        if f.startswith(resume_id):
            os.remove(os.path.join(PROCESSED_DIR, f))

    return {"message": "Resume deleted successfully"}



