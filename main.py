import base64

import streamlit as st
import streamlit.components.v1 as components

import Homepage
import auth
import graphs
import main_dashboard as dashboard
import pure_python_auth as ppa
import utils as ut


st.set_page_config(
    page_title="XYZ Bank Analytics",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={},
)

# Keep Streamlit header/menu controls available for mobile sidebar toggle.
st.markdown(
    """
    <style>
    footer {visibility: hidden;}

    [data-testid="stHeader"],
    header {
        visibility: visible !important;
        display: block !important;
    }

    /* Keep header visible, hide only GitHub/Edit actions */
    [data-testid="stToolbar"] {
        display: flex !important;
    }

    [data-testid="stToolbar"] a[href*="github.com"],
    [data-testid="stToolbar"] button[title*="Edit"],
    [data-testid="stToolbar"] button[aria-label*="Edit"],
    [data-testid="stToolbar"] button[title*="GitHub"],
    [data-testid="stToolbar"] button[aria-label*="GitHub"] {
        display: none !important;
    }

    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        width: 270px !important;
        min-width: 270px !important;
        max-width: 270px !important;
    }

    @media (min-width: 1025px) {
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            transform: translateX(0) !important;
            margin-left: 0 !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
    }

    @media (max-width: 1024px) {
        [data-testid="stSidebar"] button {
            width: 100% !important;
            margin: 0.5rem 0 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ut.apply_sidebar_styles()
ppa.init_persistent_auth()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

query_params = st.query_params
if "page" in query_params:
    st.session_state["page"] = query_params["page"]
elif "page" not in st.session_state:
    st.session_state["page"] = "Homepage"

if st.session_state.get("page") not in ["Homepage", "Dashboard", "Graphs", "Auth"]:
    st.session_state["page"] = "Homepage"


def add_sidebar_image(image_path: str) -> None:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.sidebar.markdown(
        f"""
        <div class="sidebar-image-container">
            <img src="data:image/png;base64,{encoded_string}"
                 style="max-height: 280px; width: 100%; border-radius: 8px; margin-bottom: 20px;">
        </div>
        <div class="sidebar-buttons-container">
        """,
        unsafe_allow_html=True,
    )


try:
    add_sidebar_image("images/sidebar.jpeg")
except Exception:
    st.sidebar.markdown(
        "<div class='sidebar-title' style='font-size: 24px; font-weight: bold;'>☰ Navigation</div>",
        unsafe_allow_html=True,
    )


def set_page(target_page: str) -> None:
    st.session_state["page"] = target_page
    st.session_state["collapse_sidebar_after_nav"] = True
    st.query_params.page = target_page
    st.rerun()


if st.session_state["authenticated"]:
    if st.sidebar.button("Welcome & Introduction Portal", key="go_home"):
        set_page("Homepage")
    if st.sidebar.button("Analytical Main Dashboard Page", key="go_dashboard"):
        set_page("Dashboard")
    if st.sidebar.button("Detailed Insight Visualizations", key="go_graphs"):
        set_page("Graphs")
    if st.sidebar.button("Session Termination Process ", key="logout"):
        ppa.logout_user()
        set_page("Auth")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
else:
    if st.sidebar.button("Welcome & Introduction Portal", key="go_home_guest"):
        set_page("Homepage")
    if st.sidebar.button("Access & Registration Gateway", key="go_auth"):
        set_page("Auth")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("debug_mode", False):
    st.sidebar.write(f"Current page: {st.session_state.get('page', 'None')}")
    st.sidebar.write(f"Query params: {dict(st.query_params)}")
    st.sidebar.write(f"Authenticated: {st.session_state.get('authenticated', False)}")

if st.session_state["page"] == "Homepage":
    if not st.session_state["authenticated"]:
        st.markdown(
            """
            <div style="color: #856404; background-color: #fff3cd; border-left: 6px solid #ffeeba;
            padding: 6px; border-radius: 4px; margin-bottom: 12px; font-size: 21px; width: 90%;">
                ⚠️ Please log in to access the main dashboard.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "animated_hint_shown" not in st.session_state:
            st.session_state["animated_hint_shown"] = True
            st.markdown(
                """
                <div style="background-color: #f8d7da; color: #721c24; padding: 6px 8px;
                border-radius: 6px; font-size: 21px; border-left: 6px solid #f5c6cb;
                margin-bottom: 18px; width: 90%;">
                    📢 <strong>Tap '>>' to access sidebar on mobile.</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()

elif st.session_state["page"] == "Graphs":
    if st.session_state["authenticated"]:
        graphs.main()

elif st.session_state["page"] == "Auth":
    auth.main()

if st.session_state.get("collapse_sidebar_after_nav"):
    components.html(
        """
        <script>
        (function () {
            const mq = window.parent.matchMedia('(max-width: 1024px)');
            if (!mq.matches) return;

            const doc = window.parent.document;
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;

            sidebar.setAttribute('aria-expanded', 'false');
            sidebar.style.setProperty('transform', 'translateX(-270px)', 'important');
        })();
        </script>
        """,
        height=0,
    )
    del st.session_state["collapse_sidebar_after_nav"]

# Restore mobile/tablet collapse behavior: fully retreat sidebar when collapsed.
components.html(
    """
    <script>
    (function () {
        const mq = window.parent.matchMedia('(max-width: 1024px)');
        const doc = window.parent.document;

        function normalizeMobileSidebar() {
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;

            if (!mq.matches) {
                sidebar.style.removeProperty('transform');
                return;
            }

            const expanded = sidebar.getAttribute('aria-expanded') === 'true';
            if (expanded) {
                sidebar.style.setProperty('transform', 'translateX(0px)', 'important');
            } else {
                sidebar.style.setProperty('transform', 'translateX(-270px)', 'important');
            }
        }

        normalizeMobileSidebar();

        const sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            const observer = new MutationObserver(normalizeMobileSidebar);
            observer.observe(sidebar, {
                attributes: true,
                attributeFilter: ['aria-expanded', 'style']
            });
        }

        setTimeout(normalizeMobileSidebar, 80);
        setTimeout(normalizeMobileSidebar, 200);
        window.addEventListener('resize', normalizeMobileSidebar);
    })();
    </script>
    """,
    height=0,
)
