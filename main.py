import streamlit as st
import base64
import Homepage
import auth
import main_dashboard as dashboard
import utils as ut

# --- Page config (REMOVE expanded default) ---
st.set_page_config(
    page_title="XYZ Bank Analytics",
    layout="centered"
)

# --- Session state setup ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Homepage"

# --- Optional: Only expand sidebar on desktop via JS ---
st.markdown("""
<script>
const mq = window.matchMedia("(min-width: 768px)");
if (mq.matches) {
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) sidebar.style.display = "block";
}
</script>
""", unsafe_allow_html=True)

# --- Styles from utils ---
ut.apply_sidebar_styles()

# --- Sidebar image (if any) ---
def add_sidebar_image(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.sidebar.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="data:image/png;base64,{encoded}" style="max-height: 300px;" />
            </div>
        """, unsafe_allow_html=True)
    except:
        st.sidebar.markdown("## ☰ XYZ Bank")

add_sidebar_image("sidebar.jpeg")

# --- Sidebar navigation ---
st.sidebar.markdown("### 🔹 Navigation")

if st.session_state["authenticated"]:
    if st.sidebar.button("🏠 Homepage"):
        st.session_state["page"] = "Homepage"
        st.rerun()
    if st.sidebar.button("📊 Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()
    if st.sidebar.button("🚪 Logout"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["page"] = "Homepage"
        st.rerun()
else:
    if st.sidebar.button("🏠 Homepage"):
        st.session_state["page"] = "Homepage"
        st.rerun()
    if st.sidebar.button("🔐 Login / Signup"):
        st.session_state["page"] = "Auth"
        st.rerun()

# --- Page routing ---
if st.session_state["page"] == "Homepage":
    if not st.session_state["authenticated"]:
        st.markdown("""
        <div style="color: #856404; background-color: #fff3cd; border-left: 6px solid #ffeeba; padding: 12px; border-radius: 4px;">
        ⚠️ Please log in to access the dashboard. <span style="color: #721c24; background-color: #f8d7da; padding: 2px 5px; border-radius: 3px;">Use ☰ to open the menu on mobile.</span>
        </div>
        """, unsafe_allow_html=True)
    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()
    else:
        st.warning("Please log in to access the dashboard.")

elif st.session_state["page"] == "Auth":
    auth.main()
