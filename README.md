# TalentSync — AI-Powered ATS Resume Matcher

> Match the right candidates to the right jobs in seconds.

TalentSync is a full-stack Applicant Tracking System that lets recruiters upload resumes, paste a job description, and instantly get a ranked list of best-fit candidates — with match scores, skills, and experience highlights.

---

## What it does

- **Upload resumes** (PDF or DOCX) into a public or private company database
- **Paste any job description** and get back candidates ranked by match score
- **Vector search + cosine reranking** for accurate semantic matching without relying on keyword overlap
- **Analytics dashboard** — visualize top skills, resume counts, and public vs private splits
- **JWT auth** — secure recruiter accounts with access + refresh token flow

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Database | MongoDB |
| Vector Store | ChromaDB (persistent) |
| Embeddings | Hash-based sparse embeddings (no GPU needed) |
| Auth | JWT (python-jose + bcrypt) |
| Resume Parsing | pdfplumber, python-docx |
| Charts | Plotly |

---

## Project Structure

```
AI-JD-RESUME/
├── main.py               # FastAPI app entrypoint
├── app.py                # Streamlit entrypoint
├── config.py             # Env-based config
├── database.py           # MongoDB client + indexes
├── chroma_client.py      # ChromaDB persistent client
├── embedding.py          # Deterministic hash embedding (384-dim)
├── llm_parser.py         # Resume skill/experience/education extractor
├── reranker.py           # Cosine similarity reranker
├── jd_matcher.py         # JD → vector search → rerank pipeline
├── resume_service.py     # Upload / update / delete resume logic
├── resume_routes.py      # /resumes/* API routes
├── jd_routes.py          # /jd/match API route
├── auth_routes.py        # /auth/signup, /auth/login, /auth/refresh
├── auth_service.py       # Recruiter signup/login logic
├── auth_utils.py         # JWT + bcrypt helpers
├── utils.py              # PDF/DOCX text extraction
├── models.py             # Pydantic models
├── dependencies.py       # FastAPI auth dependency
└── frontend/
    ├── api.py            # HTTP client for backend
    ├── auth.py           # Login / signup page
    ├── dashboard.py      # Resume list + stats cards
    ├── upload.py         # Resume upload page
    ├── jd_match.py       # JD matching page
    ├── analytics.py      # Plotly charts page
    └── styles.py         # Custom CSS injection
```

---

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/slayerkkkkkkk/AI-JD-RESUME.git
cd AI-JD-RESUME
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
JWT_SECRET=your-long-random-secret
MONGO_URI=mongodb://localhost:27017
DB_NAME=AI_Resume
OPENAI_API_KEY=sk-...        # optional — only if you swap in GPT parsing
API_BASE_URL=http://127.0.0.1:8000
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MIN=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> MongoDB must be running locally. Download from [mongodb.com](https://www.mongodb.com/try/download/community).

### 3. Create data directories

```bash
mkdir -p data/raw_resumes data/processed_resumes data/chromadb
```

### 4. Start the backend

```bash
python -m uvicorn main:app --reload --port 8000
```

### 5. Start the frontend

```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## API Reference

Interactive docs available at **http://localhost:8000/docs**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register a recruiter account |
| POST | `/auth/login` | Login and get JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/resumes/upload` | Upload one or more resumes |
| GET | `/resumes/list` | List all uploaded resumes |
| GET | `/resumes/stats` | Get counts and top skills |
| PUT | `/resumes/{id}` | Replace a resume file |
| DELETE | `/resumes/{id}` | Delete a resume |
| POST | `/jd/match` | Match a JD against the resume database |

---

## How Matching Works

1. Resume text is extracted from PDF/DOCX and cleaned
2. Skills, experience lines, and education are parsed via regex
3. A 384-dimensional hash embedding is generated for each resume and stored in ChromaDB
4. When a JD is submitted, the same embedding is generated for the JD text
5. ChromaDB returns the top 10 nearest resumes by vector similarity
6. A cosine reranker re-scores and sorts the results
7. Final candidates are returned with name, skills, experience, and match score (%)

---

## License

MIT
