import base64

import streamlit as st

import Homepage
import auth
import graphs
import main_dashboard as dashboard
import pure_python_auth as ppa
import utils as ut
from walkthrough_ui import render_coachmark


st.set_page_config(
    page_title="XYZ Bank Analytics",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={},
)

# Keep Streamlit header/menu controls available for smaller devices sidebar toggle.
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

valid_walkthrough_steps = {
    "account_access", "account_options", "customer_form",
    "customer_graphs", "logout_tip", "complete",
}
if st.session_state.get("walkthrough_step") not in valid_walkthrough_steps:
    if st.session_state["authenticated"]:
        current_page = st.session_state["page"]
        st.session_state["walkthrough_step"] = {
            "Homepage": "customer_form",
            "Graphs": "logout_tip",
            "Dashboard": "customer_form",
            "Auth": "complete",
        }[current_page]
    else:
        st.session_state["walkthrough_step"] = (
            "account_options" if st.session_state["page"] == "Auth" else "account_access"
        )


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
    st.session_state["collapse_sidebar_after_navigation"] = True
    st.query_params.page = target_page
    st.rerun()


if st.session_state["authenticated"]:
    if st.sidebar.button("Welcome & Introduction Portal", key="go_home"):
        set_page("Homepage")
    if st.sidebar.button("Analytical Main Dashboard Page", key="go_dashboard"):
        set_page("Dashboard")
    if (
        st.session_state.get("walkthrough_step") == "customer_form"
        and st.session_state.get("page") != "Dashboard"
    ):
        render_coachmark(
            "Start with the dashboard",
            "Choose Analytical Main Dashboard Page to enter customer details and view the prediction.",
            container=st.sidebar,
            placement="sidebar",
        )
        render_coachmark(
            "Open the sidebar",
            "Tap the top-left chevrons, then choose Analytical Main Dashboard Page.",
            placement="edge",
        )
    if st.sidebar.button("Detailed Insight Visualizations", key="go_graphs"):
        if st.session_state.get("walkthrough_step") == "customer_graphs":
            st.session_state["walkthrough_step"] = "logout_tip"
        set_page("Graphs")
    if st.session_state.get("walkthrough_step") == "customer_graphs":
        render_coachmark(
            "Next, explore customer graphs",
            "Choose Detailed Insight Visualizations to compare customer trends after reviewing the prediction.",
            container=st.sidebar,
            placement="sidebar",
        )
        render_coachmark(
            "Open the sidebar",
            "Tap the top-left chevrons, then choose Detailed Insight Visualizations.",
            placement="edge",
        )
    if st.sidebar.button("Session Termination Process ", key="logout"):
        st.session_state["walkthrough_step"] = "complete"
        ppa.logout_user()
        set_page("Auth")
    if st.session_state.get("walkthrough_step") == "logout_tip":
        render_coachmark(
            "Finish your session",
            "Your prediction and explanation are on this page. Choose Session Termination Process when you’re ready to log out.",
            container=st.sidebar,
            placement="sidebar",
        )
        render_coachmark(
            "Open the sidebar",
            "Tap the top-left chevrons, then choose Session Termination Process to log out.",
            placement="edge",
        )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
else:
    if st.sidebar.button("Welcome & Introduction Portal", key="go_home_guest"):
        set_page("Homepage")
    if st.sidebar.button("Access & Registration Gateway", key="go_auth"):
        if st.session_state.get("walkthrough_step") == "account_access":
            st.session_state["walkthrough_step"] = "account_options"
        set_page("Auth")
    if st.session_state.get("walkthrough_step") == "account_access":
        render_coachmark(
            "Log in or create an account",
            "Choose this button to log in, sign up, or reset your password.",
            container=st.sidebar,
            placement="sidebar",
        )
        render_coachmark(
            "Open the navigation",
            "Tap the chevrons at the top-left to open the sidebar and find Log in or sign up.",
            placement="edge",
        )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("debug_mode", False):
    st.sidebar.write(f"Current page: {st.session_state.get('page', 'None')}")
    st.sidebar.write(f"Query params: {dict(st.query_params)}")
    st.sidebar.write(f"Authenticated: {st.session_state.get('authenticated', False)}")

if st.session_state["page"] == "Homepage":
    Homepage.main()

elif st.session_state["page"] == "Dashboard":
    if st.session_state["authenticated"]:
        dashboard.main()

elif st.session_state["page"] == "Graphs":
    if st.session_state["authenticated"]:
        graphs.main()

elif st.session_state["page"] == "Auth":
    auth.main()

if st.session_state.pop("collapse_sidebar_after_navigation", False):
    st.iframe(
        """
        <script>
        if (window.parent.matchMedia('(max-width: 1024px)').matches) {
            const collapseButton = window.parent.document.querySelector(
                '[data-testid="stSidebarCollapseButton"] button'
            );
            if (collapseButton) collapseButton.click();
        }
        </script>
        """,
        width=1,
        height=1,
        tab_index=-1,
    )

