import streamlit as st
import Homepage
import auth
import main_dashboard as dashboard
import base64
import graphs 
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
[data-testid="collapse-control"] {
    margin-top: 34px !important;
}
[data-testid="stSidebar"] {
    padding-top: 3.5rem !important;
}
.streamlit-alert {
    width: 55% !important;
    font-size: 21px !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Init Session ----
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "Homepage"
    st.session_state["first_visit"] = True

# Trigger sidebar collapse on very first load on mobile
if st.session_state.get("first_visit"):
    st.session_state["force_sidebar_collapse"] = True
    del st.session_state["first_visit"]


# ---- Sidebar Image ----
def add_sidebar_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div class="sidebar-image-container">
            <img src="data:image/png;base64,{encoded_string}" 
            style="max-height: 280px; width: 100%; border-radius: 8px;margin-bottom: 20px;">
        </div>
        """,
        unsafe_allow_html=True
    )

try:
    add_sidebar_image('images/sidebar.jpeg')
except:
    st.sidebar.markdown("<div class='sidebar-title' style='font-size: 24px; font-weight: bold;'>☰ Navigation</div>", unsafe_allow_html=True)

# ---- Navigation Logic ----
def set_page(target_page):
    st.session_state["page"] = target_page
    st.session_state["force_sidebar_collapse"] = True
    st.rerun()

if st.session_state["authenticated"]:
    if st.sidebar.button("🏠 HOMEPAGE", key="go_home"):
        set_page("Homepage")
    if st.sidebar.button("📊 DASHBOARD", key="go_dashboard"):
        set_page("Dashboard")
    if st.sidebar.button("📈 GRAPHS", key="go_graphs"):
        set_page("Graphs")
    if st.sidebar.button("🚪 LOGOUT", key="logout"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        set_page("Auth")
else:
    if st.sidebar.button("🏠 HOMEPAGE", key="go_home_guest"):
        set_page("Homepage")
    if st.sidebar.button("🔐 LOGIN/SIGNUP", key="go_auth"):
        set_page("Auth")

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
elif st.session_state["page"] == "Graphs":
    if st.session_state["authenticated"]:
        graphs.main()

elif st.session_state["page"] == "Auth":
    auth.main()

# ---- Inject Sidebar Collapse (mobile only) ----
if st.session_state.get("force_sidebar_collapse"):
    components.html("""
    <script>
    const mq = window.matchMedia("(max-width: 768px)");
    if (mq.matches) {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.setAttribute("aria-expanded", "false");
        }
    }
    </script>
    """, height=0)
    del st.session_state["force_sidebar_collapse"]