import streamlit as st
import requests
from frontend.api import signup, login

def auth_page():
    st.title("🔐 TalentSync – Recruiter Access")

    # Check if backend is reachable first
    from frontend.api import BASE_URL
    try:
        requests.get(f"{BASE_URL}/docs", timeout=5)
    except Exception:
        st.error("⚠️ Backend is not running. Please start it first:")
        st.code("python -m uvicorn main:app --reload --port 8000", language="bash")
        st.info("Open a new terminal, run the command above, then refresh this page.")
        st.stop()

    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "Login"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.auth_tab = "Login"
    with col2:
        if st.button("Signup"):
            st.session_state.auth_tab = "Signup"

    st.markdown("---")

    if st.session_state.auth_tab == "Login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login Now"):
            try:
                res = login(email, password)
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Backend stopped. Run: python -m uvicorn main:app --reload --port 8000")

    else:
        email = st.text_input("Signup Email", key="signup_email")
        password = st.text_input("Signup Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            try:
                res = signup(email, password)
                if res.status_code == 200:
                    st.success("Signup successful. Please login.")
                    st.session_state.auth_tab = "Login"
                else:
                    st.error(res.text)
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Backend stopped. Run: python -m uvicorn main:app --reload --port 8000")
