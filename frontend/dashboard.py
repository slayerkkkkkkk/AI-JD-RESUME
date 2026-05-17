import streamlit as st
from frontend.api import get_resumes, get_stats
from frontend.styles import inject_custom_css

def dashboard():
    inject_custom_css()
    st.title("🧠 TalentSync Recruiter Dashboard")

    token = st.session_state.get("token")

    # Fetch stats
    stats_res = get_stats(token)
    if stats_res.status_code == 200:
        stats = stats_res.json()
        total = stats.get("total", 0)
        public = stats.get("public", 0)
        private = stats.get("private", 0)
    else:
        total = public = private = 0

    # Summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Total Resumes", total)
    with col2:
        st.metric("🌐 Public", public)
    with col3:
        st.metric("🔒 Private", private)

    st.markdown("---")

    # Recent resumes table
    st.subheader("📋 Uploaded Resumes")
    resumes_res = get_resumes(token)
    if resumes_res.status_code == 200:
        resumes = resumes_res.json()
        if not resumes:
            st.info("No resumes uploaded yet. Go to Upload Resumes to get started.")
        else:
            for r in resumes:
                with st.expander(f"👤 {r.get('name', 'Unknown')}  —  {r.get('visibility', '').capitalize()}"):
                    skills = r.get("skills", [])
                    st.write("**Skills:**", ", ".join(skills) if skills else "N/A")
                    st.write("**Experience:**", r.get("experience") or "N/A")
                    if r.get("company"):
                        st.write("**Company:**", r["company"])
                    st.caption(f"Resume ID: {r.get('resume_id')} | Uploaded: {r.get('uploaded_at', '')[:10]}")
    else:
        st.error("Could not load resumes from server.")
