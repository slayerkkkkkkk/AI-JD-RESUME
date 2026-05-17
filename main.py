# from fastapi import FastAPI, Depends
# from models import ResumeUpload, JDRequest
# from resume_service import upload_resume
# from jd_matcher import match_jd
# from auth_routes import router as auth_router
# from dependencies import get_current_recruiter
# from resume_routes import router as resume_router

# app = FastAPI(title="ATS Resume Matcher")
# app.include_router(auth_router)
# app.include_router(resume_router) 


# def get_recruiter_id():
#     return "recruiter_123"  # from JWT in real system

# @app.post("/resumes/upload")
# def upload(resume: ResumeUpload, recruiter_id=Depends(get_recruiter_id)):
#     return {
#         "resume_id": upload_resume(
#             resume.resume_text,
#             resume.visibility,
#             recruiter_id
#         )
#     }

# @app.post("/jd/match")
# def match_jd_route(jd: JDRequest, recruiter_id=Depends(get_recruiter_id)):
#     return match_jd(
#         jd.jd_text,
#         jd.db_type,
        
#     )

from contextlib import asynccontextmanager
from fastapi import FastAPI
from resume_routes import router as resume_router
from jd_routes import router as jd_router
from auth_routes import router as auth_router
from database import ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_indexes()
    yield


app = FastAPI(title="AI ATS Resume Matcher", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(jd_router)

