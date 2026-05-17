import streamlit as st
import plotly.express as px
import pandas as pd
from frontend.api import get_stats

def analytics_page():
    st.header("📊 Resume Analytics")

    token = st.session_state.get("token")
    res = get_stats(token)

    if res.status_code != 200:
        st.error("Could not load analytics data.")
        return

    stats = res.json()
    total = stats.get("total", 0)
    public = stats.get("public", 0)
    private = stats.get("private", 0)
    top_skills = stats.get("top_skills", [])

    if total == 0:
        st.info("No resumes uploaded yet. Upload some resumes to see analytics.")
        return

    col1, col2 = st.columns(2)

    # Pie chart — visibility
    with col1:
        pie_df = pd.DataFrame({
            "Category": ["Public", "Private"],
            "Count": [public, private]
        })
        fig = px.pie(pie_df, values="Count", names="Category",
                     title="Resume Visibility", hole=0.4,
                     color_discrete_sequence=["#14b8a6", "#0ea5e9"])
        st.plotly_chart(fig, use_container_width=True)

    # Bar chart — top skills
    with col2:
        if top_skills:
            skill_df = pd.DataFrame(top_skills)
            bar = px.bar(skill_df, x="skill", y="count",
                         title="Top Skills Across All Resumes",
                         color="count",
                         color_continuous_scale="teal")
            bar.update_layout(showlegend=False)
            st.plotly_chart(bar, use_container_width=True)
        else:
            st.info("No skill data available yet.")

    # Summary numbers
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Resumes", total)
    c2.metric("Public", public)
    c3.metric("Private", private)
