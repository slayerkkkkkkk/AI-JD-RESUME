import sys
import os

# Add project root to path so "frontend.xxx" imports resolve
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from frontend.auth import auth_page
from frontend.dashboard import dashboard
from frontend.upload import upload_page
from frontend.jd_match import jd_page
from frontend.analytics import analytics_page
from frontend.styles import inject_custom_css

st.set_page_config(
    page_title="TalentSync",
    page_icon="🧠",
    layout="wide"
)

inject_custom_css()

if "token" not in st.session_state:
    st.session_state.token = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = True

if st.session_state.token is None:
    auth_page()
else:
    st.session_state.auth_page = False

    st.sidebar.title("TalentSync")
    choice = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Upload Resumes", "JD Matching", "Analytics", "Logout"]
    )

    if choice == "Dashboard":
        dashboard()
    elif choice == "Upload Resumes":
        upload_page()
    elif choice == "JD Matching":
        jd_page()
    elif choice == "Analytics":
        analytics_page()
    else:
        st.session_state.token = None
        st.rerun()
