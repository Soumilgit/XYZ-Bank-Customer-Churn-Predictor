# main.py
import streamlit as st
import Homepage
import auth
import main_dashboard as dashboard  # renamed to avoid conflict with main.py itself


st.set_page_config(page_title="XYZ Bank Analytics", layout="centered")

import utils as ut
ut.apply_sidebar_styles()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Homepage"

# Sidebar navigation UI
st.sidebar.markdown("""
<style>
.sidebar-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333;
}
.sidebar-btn {
    width: 100%;
    padding: 0.5rem 1rem;
    margin: 0.3rem 0;
    text-align: center;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    background-color: #007BFF;
    color: white;
    cursor: pointer;
}
.sidebar-btn:hover {
    background-color: #0056b3;
}
</style>
<div class='sidebar-title'>☰ Navigation</div>
""", unsafe_allow_html=True)

if st.session_state["authenticated"]:
    if st.sidebar.button("🏠 HOMEPAGE", key="go_home"):
        st.session_state["page"] = "Homepage"
        st.rerun()
    if st.sidebar.button("📊 DASHBOARD", key="go_dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()
    if st.sidebar.button("🚪 LOGOUT", key="logout"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["page"] = "Auth"
        st.rerun()
else:
    if st.sidebar.button("🏠 HOMEPAGE", key="go_home_guest"):
        st.session_state["page"] = "Homepage"
        st.rerun()
    if st.sidebar.button("🔐 LOGIN/SIGNUP", key="go_auth"):
        st.session_state["page"] = "Auth"
        st.rerun()

# Router to switch pages
if st.session_state["page"] == "Homepage":
    if not st.session_state["authenticated"]:
        st.markdown("""
        <div style="color: #856404; background-color: #fff3cd; border-left: 6px solid #ffeeba; padding: 12px; border-radius: 4px;">
        ⚠️ Please log in to access the dashboard.
        </div>
        """, unsafe_allow_html=True)
    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()
    

elif st.session_state["page"] == "Auth":
    auth.main()
