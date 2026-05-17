import re

SKILLS_LIST = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php",
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring", "express",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "linux", "git",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "opencv", "keras",
    "html", "css", "tailwind", "bootstrap", "graphql", "rest", "api",
    "agile", "scrum", "ci/cd", "devops", "microservices"
]

def parse_resume(text: str) -> dict:
    lower = text.lower()

    # Extract name — first non-empty line that looks like a name
    name = None
    for line in text.splitlines():
        line = line.strip()
        if 2 < len(line) < 40 and re.match(r"^[A-Za-z\s\.\-]+$", line):
            name = line
            break

    # Extract skills by keyword match
    found_skills = [s for s in SKILLS_LIST if s in lower]

    # Extract experience snippets — lines mentioning years or job titles
    exp_lines = []
    for line in text.splitlines():
        l = line.strip()
        if re.search(r"\b(engineer|developer|manager|analyst|intern|lead|architect|designer)\b", l, re.I):
            if 10 < len(l) < 120:
                exp_lines.append(l)
        if re.search(r"\b(20\d{2})\b", l):
            if 10 < len(l) < 120 and l not in exp_lines:
                exp_lines.append(l)

    # Extract education snippets
    edu_lines = []
    for line in text.splitlines():
        l = line.strip()
        if re.search(r"\b(bachelor|master|b\.?tech|m\.?tech|b\.?e|mba|phd|degree|university|college|school)\b", l, re.I):
            if 5 < len(l) < 150:
                edu_lines.append(l)

    return {
        "name": name or "Unknown",
        "skills": found_skills if found_skills else ["Not detected"],
        "experience": " | ".join(exp_lines[:5]) if exp_lines else "Not detected",
        "education": " | ".join(edu_lines[:3]) if edu_lines else "Not detected",
        "projects": []
    }
