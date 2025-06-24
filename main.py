import streamlit as st
import Homepage
import auth
import main_dashboard as dashboard  # renamed to avoid conflict with main.py itself
import base64
import utils as ut

st.set_page_config(page_title="XYZ Bank Analytics", layout="centered")

ut.apply_sidebar_styles()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Homepage"

def add_sidebar_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{encoded_string}" style="max-height: 450px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar fallback if image fails
try:
    add_sidebar_image('sidebar.jpeg')
except:
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px; font-size: 24px; font-weight: bold;'>
    ☰ Navigation
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
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
""", unsafe_allow_html=True)

# Sidebar content based on login
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

# Page Routing
if st.session_state["page"] == "Homepage":
    if not st.session_state["authenticated"]:
        # Yellow warning
        st.markdown("""
        <div style="color: #856404; background-color: #fff3cd; border-left: 6px solid #ffeeba;
        padding: 12px; border-radius: 4px; margin-bottom: 12px;font-size: 26px;">
            ⚠️ Please login to access the dashboard.
        </div>
        """, unsafe_allow_html=True)

        # Red box below yellow, zoom animated once
        if "animated_hint_shown" not in st.session_state:
            st.session_state["animated_hint_shown"] = True
            st.markdown("""
            <div class="zoom-box">
                📢 <strong>Use '≫' at the top-left to open the menu and login.</strong>
            </div>
            <style>
            .zoom-box {
                background-color: #f8d7da;
                color: #721c24;
                padding: 14px 20px;
                border-radius: 6px;
                font-size: 26px;
                border-left: 6px solid #f5c6cb;
                margin-bottom: 24px;
                animation: zoomIn 0.6s ease;
            }
            @keyframes zoomIn {
                0% {
                    opacity: 0;
                    transform: scale(0.8);
                }
                100% {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            </style>
            """, unsafe_allow_html=True)

    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()

elif st.session_state["page"] == "Auth":
    auth.main()
