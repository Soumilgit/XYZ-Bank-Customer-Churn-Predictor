import streamlit as st
import Homepage
import auth
import main_dashboard as dashboard
import base64
import utils as ut
import streamlit.components.v1 as components

# ---- Page Config ----
st.set_page_config(
    page_title="XYZ Bank Analytics",
    page_icon="🔄", 
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={}
)

ut.apply_sidebar_styles()

# ---- CSS: Sidebar behavior & responsiveness ----
st.markdown("""
<style>
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        transform: translateX(-100%);
        transition: transform 0s ease-in-out;
        position: fixed;
        z-index: 100;
        width: 270px !important;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        transform: translateX(0);
    }
    [data-testid="stSidebarResizer"] {
        display: none !important;
    }
}

/* Move the collapse < button lower */
[data-testid="collapse-control"] {
    margin-top: 34px !important;
}

/* Prevent header overlap */
[data-testid="stSidebar"] {
    padding-top: 3.5rem !important;
}

/* Adjust popup width and font size */
.streamlit-alert {
    width: 55% !important;
    font-size: 21px !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Session State Init ----
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Homepage"

# ---- Sidebar Image ----
# ---- Sidebar Image ----
def add_sidebar_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div class="sidebar-image-container">
            <img src="data:image/png;base64,{encoded_string}" style="max-height: 280px; width: 100%; border-radius: 8px;margin-bottom: 20px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- Sidebar Header ----
try:
    add_sidebar_image('sidebar.jpeg')
except:
    st.sidebar.markdown("""
    <div class="sidebar-title" style='font-size: 24px; font-weight: bold;'>
    ☰ Navigation
    </div>
    """, unsafe_allow_html=True)

# ---- Sidebar Navigation ----
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

# ---- Page Routing ----
if st.session_state["page"] == "Homepage":
    if not st.session_state["authenticated"]:
        st.markdown("""
        <div style="color: #856404; background-color: #fff3cd; border-left: 6px solid #ffeeba;
        padding: 6px; border-radius: 4px; margin-bottom: 12px; font-size: 21px; width: 90%;">
            ⚠️ Please log in to access the main dashboard.
        </div>
        """, unsafe_allow_html=True)

        if "animated_hint_shown" not in st.session_state:
            st.session_state["animated_hint_shown"] = True
            st.markdown("""
            <div style="background-color: #f8d7da; color: #721c24; padding: 6px 8px;
            border-radius: 6px; font-size: 21px; border-left: 6px solid #f5c6cb;
            margin-bottom: 18px; width: 90%;">
                📢 <strong>Use '≫', top-left, to open sidebar via mobile.</strong>
            </div>
            """, unsafe_allow_html=True)
    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()

elif st.session_state["page"] == "Auth":
    auth.main()

# ---- Auto-collapse sidebar on mobile after any navigation ----
components.html("""
<script>
window.addEventListener("load", function() {
    const mq = window.matchMedia("(max-width: 768px)");
    if (mq.matches) {
        setTimeout(() => {
            const root = window.parent.document;
            const sidebar = root.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.setAttribute("aria-expanded", "false");
            }
        }, 120);
    }
});
</script>
""", height=0)