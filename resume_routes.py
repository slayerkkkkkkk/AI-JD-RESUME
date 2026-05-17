from typing import List, Optional

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from resume_service import (
    upload_resumes_service,
    update_resume_service,
    delete_resume_service
)

from dependencies import get_current_recruiter

from database import processed_resumes as processed_col

router = APIRouter(prefix="/resumes", tags=["Resumes"])


# ======================= UPLOAD =======================

@router.post("/upload")
async def upload_resumes(
    files: List[UploadFile] = File(...),
    visibility: str = Form(...),      # public | private
    company: Optional[str] = Form(None),
    # recruiter_id: Optional[str] = Depends(get_current_recruiter)
):
    try:
        return upload_resumes_service(
            files=files,
            visibility=visibility,
            company=company,
            recruiter_id=None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ======================= LIST =======================

@router.get("/list")
def list_resumes():
    docs = list(processed_col.find({}, {"_id": 0, "resume_id": 1, "structured": 1, "visibility": 1, "company": 1, "uploaded_at": 1}))
    results = []
    for d in docs:
        structured = d.get("structured") or {}
        results.append({
            "resume_id": d.get("resume_id"),
            "name": structured.get("name", "Unknown"),
            "skills": structured.get("skills", []),
            "experience": structured.get("experience", ""),
            "visibility": d.get("visibility"),
            "company": d.get("company"),
            "uploaded_at": str(d.get("uploaded_at", ""))
        })
    return results


# ======================= STATS =======================

@router.get("/stats")
def resume_stats():
    total = processed_col.count_documents({})
    public = processed_col.count_documents({"visibility": "public"})
    private = processed_col.count_documents({"visibility": "private"})

    # Top skills across all resumes
    skill_counts: dict = {}
    for doc in processed_col.find({}, {"structured.skills": 1}):
        skills = (doc.get("structured") or {}).get("skills", [])
        for s in skills:
            skill_counts[s] = skill_counts.get(s, 0) + 1

    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total": total,
        "public": public,
        "private": private,
        "top_skills": [{"skill": s, "count": c} for s, c in top_skills]
    }


# ======================= UPDATE =======================

@router.put("/{resume_id}")
async def update_resume(
    resume_id: str,
    file: UploadFile = File(...),
    recruiter_id: str = Depends(get_current_recruiter)
):
    try:
        return update_resume_service(
            resume_id=resume_id,
            file=file,
            recruiter_id=recruiter_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======================= DELETE =======================

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    recruiter_id: str = Depends(get_current_recruiter)
):
    try:
        return delete_resume_service(
            resume_id=resume_id,
            recruiter_id=recruiter_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



