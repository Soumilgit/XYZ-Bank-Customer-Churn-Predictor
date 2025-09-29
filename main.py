import streamlit as st
import Homepage
import auth
import main_dashboard as dashboard
import base64
import graphs 
import utils as ut
import streamlit.components.v1 as components
import pure_python_auth as ppa

st.set_page_config(
    page_title="XYZ Bank Analytics",
    page_icon="🔄", 
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.markdown("""
<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
.viewerBadge_text__1JaDK {
    display: none;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

ut.apply_sidebar_styles()

st.markdown("""
<style>
/* Desktop styles - FORCE sidebar to always be visible with maximum specificity */
@media (min-width: 769px) {
    /* Target all possible sidebar states on desktop */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"][aria-expanded="false"],
    [data-testid="stSidebar"][aria-expanded="true"],
    [data-testid="stSidebar"]:not([aria-expanded]),
    .css-1d391kg,
    .css-1cypcdb,
    .css-17eq0hr,
    section[data-testid="stSidebar"] {
        transform: translateX(0px) !important;
        margin-left: 0px !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        visibility: visible !important;
        opacity: 1 !important;
        width: 16rem !important;
        min-width: 16rem !important;
        max-width: 16rem !important;
        left: 0px !important;
        right: auto !important;
        top: 0px !important;
        height: auto !important;
        z-index: auto !important;
        
    }
    
    /* Override any Streamlit collapse classes */
    .css-1d391kg.e1fqkh3o0,
    .css-1cypcdb.e1fqkh3o0,
    .css-17eq0hr.e1fqkh3o0 {
        transform: translateX(0px) !important;
        margin-left: 0px !important;
        width: 16rem !important;
        display: flex !important;
    }
    
    /* Force sidebar content to be visible */
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] .css-1d391kg > div,
    [data-testid="stSidebar"] .element-container {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Hide collapse button on desktop */
    [data-testid="collapsedControl"],
    .css-1rs6os,
    .css-vk3wp9 {
        display: none !important;
    }
}

/* Mobile styles */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        transform: translateX(-100%);
        transition: transform 150ms ease-in-out;
        position: fixed;
        z-index: 100;
        width: 270px !important;
        height: 100vh !important;
        top: 0 !important;
        left: 0 !important;
        padding: 1rem !important;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        transform: translateX(0);
    }
    [data-testid="stSidebarResizer"] {
        display: none !important;
    }
    [data-testid="stSidebar"] button {
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    [data-testid="collapsedControl"] {
        margin-top: 34px !important;
        display: flex !important;
        justify-content: flex-start !important;
        padding-left: 1rem !important;
    }
    [data-testid="stSidebar"] {
        padding-top: 3.5rem !important;
    }
    .main .block-container {
        padding-top: 2rem !important;
    }
    
    [data-testid="stSidebar"]:not([aria-expanded="true"]) {
        transform: translateX(-100%) !important;
    }
}
</style>
""", unsafe_allow_html=True)

ppa.init_persistent_auth()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

query_params = st.query_params
if "page" in query_params:
    st.session_state["page"] = query_params["page"]
elif "page" not in st.session_state:
    st.session_state["page"] = "Homepage"
    st.session_state["first_visit"] = True

if st.session_state.get("page") not in ["Homepage", "Dashboard", "Graphs", "Auth"]:
    st.session_state["page"] = "Homepage"

st.session_state["force_sidebar_collapse"] = True

if st.session_state.get("first_visit"):
    del st.session_state["first_visit"]

def add_sidebar_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div class="sidebar-image-container">
            <img src="data:image/png;base64,{encoded_string}" 
            style="max-height: 280px; width: 100%; border-radius: 8px;margin-bottom: 20px;">
        </div>
        <div class="sidebar-buttons-container">
        """,
        unsafe_allow_html=True
    )

try:
    add_sidebar_image('images/sidebar.jpeg')
except:
    st.sidebar.markdown("<div class='sidebar-title' style='font-size: 24px; font-weight: bold;'>☰ Navigation</div>", unsafe_allow_html=True)

def set_page(target_page):
    st.session_state["page"] = target_page
    st.session_state["force_sidebar_collapse"] = True
    st.query_params.page = target_page
    st.rerun()

if st.session_state["authenticated"]:
    if st.sidebar.button("Welcome & Introduction Portal", key="go_home"):
        set_page("Homepage")
    if st.sidebar.button("Analytical Main Dashboard Page", key="go_dashboard"):
        set_page("Dashboard")
    if st.sidebar.button("Detailed Insight Visualizations", key="go_graphs"):
        set_page("Graphs")
    if st.sidebar.button("Session Termination Process" + " ", key="logout"):
        ppa.logout_user()
        st.session_state["immediate_logout"] = True
        set_page("Auth")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)  # Close container
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
                📢 <strong>Tap halved top blue box for mobile's sidebar.</strong>
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

if st.session_state.get("force_sidebar_collapse"):
    components.html("""
    <script>
    function handleSidebarResponsive() {
        const mq = window.matchMedia("(max-width: 768px)");
        
        // Find sidebar with multiple selectors
        let sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]') ||
                     window.parent.document.querySelector('.css-1d391kg') ||
                     window.parent.document.querySelector('section[data-testid="stSidebar"]');
        
        const collapseControl = window.parent.document.querySelector('[data-testid="collapsedControl"]');
        
        if (mq.matches) {
            // Mobile view - collapse sidebar
            if (sidebar) {
                sidebar.setAttribute("aria-expanded", "false");
                if (collapseControl) {
                    collapseControl.style.marginTop = '0.5rem';
                    collapseControl.style.marginLeft = '0.5rem';
                    collapseControl.style.setProperty('display', 'flex', 'important');
                }
            }
        } else {
            // Desktop view - FORCE sidebar to be visible with maximum strength
            if (sidebar) {
                sidebar.setAttribute("aria-expanded", "true");
                sidebar.removeAttribute("aria-hidden");
                
                // Use setProperty with important flag for maximum override strength
                sidebar.style.setProperty('transform', 'translateX(0px)', 'important');
                sidebar.style.setProperty('display', 'flex', 'important');
                sidebar.style.setProperty('visibility', 'visible', 'important');
                sidebar.style.setProperty('opacity', '1', 'important');
                sidebar.style.setProperty('width', '21rem', 'important');
                sidebar.style.setProperty('margin-left', '0px', 'important');
                sidebar.style.setProperty('position', 'relative', 'important');
                
                if (collapseControl) {
                    collapseControl.style.setProperty('display', 'none', 'important');
                }
            }
        }
    }
    
    // Listen for viewport changes
    const mediaQuery = window.matchMedia("(max-width: 768px)");
    mediaQuery.addListener(handleSidebarResponsive);
    
    // Execute multiple times with delays to catch any timing issues
    handleSidebarResponsive();
    document.addEventListener('DOMContentLoaded', handleSidebarResponsive);
    setTimeout(handleSidebarResponsive, 50);
    setTimeout(handleSidebarResponsive, 150);
    setTimeout(handleSidebarResponsive, 300);
    setTimeout(handleSidebarResponsive, 500);
    </script>
    """, height=0)
    del st.session_state["force_sidebar_collapse"]

if st.session_state.get("immediate_logout"):
    components.html("""
    <script>
    function handleSidebarOnLogout() {
        const mq = window.matchMedia("(max-width: 768px)");
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        const collapseControl = window.parent.document.querySelector('[data-testid="collapsedControl"]');
        
        if (mq.matches) {
            // Mobile view - collapse sidebar
            if (sidebar) {
                sidebar.setAttribute("aria-expanded", "false");
                sidebar.style.transform = "translateX(-100%)";
                sidebar.style.transition = "transform 150ms ease-in-out";
                if (collapseControl) {
                    collapseControl.style.marginTop = '0.5rem';
                    collapseControl.style.marginLeft = '0.5rem';
                }
            }
        } else {
            // Desktop view - keep sidebar visible even after logout
            if (sidebar) {
                sidebar.style.transform = "translateX(0)";
                sidebar.style.display = "block";
                sidebar.style.visibility = "visible";
                sidebar.style.opacity = "1";
                sidebar.setAttribute("aria-expanded", "true");
                if (collapseControl) {
                    collapseControl.style.marginTop = '';
                    collapseControl.style.marginLeft = '';
                }
            }
        }
    }
    
    handleSidebarOnLogout();
    setTimeout(handleSidebarOnLogout, 50);
    setTimeout(handleSidebarOnLogout, 100);
    setTimeout(handleSidebarOnLogout, 200);
    </script>
    """, height=0)
    del st.session_state["immediate_logout"]

# AGGRESSIVE Global sidebar monitor - ensures sidebar NEVER disappears on desktop
components.html("""
<script>
function aggressiveSidebarMonitor() {
    const mq = window.matchMedia("(max-width: 768px)");
    
    function forceDesktopSidebarVisible() {
        if (!mq.matches) { // Desktop view only
            // Get all possible sidebar selectors
            const sidebarSelectors = [
                '[data-testid="stSidebar"]',
                '.css-1d391kg',
                'section[data-testid="stSidebar"]',
                '.css-1cypcdb',
                '.css-17eq0hr'
            ];
            
            let sidebar = null;
            for (let selector of sidebarSelectors) {
                sidebar = window.parent.document.querySelector(selector);
                if (sidebar) break;
            }
            
            if (sidebar) {
                // FORCE all possible properties to make sidebar visible
                sidebar.style.setProperty('transform', 'translateX(0px)', 'important');
                sidebar.style.setProperty('margin-left', '0px', 'important');
                sidebar.style.setProperty('display', 'flex', 'important');
                sidebar.style.setProperty('flex-direction', 'column', 'important');
                sidebar.style.setProperty('visibility', 'visible', 'important');
                sidebar.style.setProperty('opacity', '1', 'important');
                sidebar.style.setProperty('width', '21rem', 'important');
                sidebar.style.setProperty('min-width', '21rem', 'important');
                sidebar.style.setProperty('max-width', '21rem', 'important');
                sidebar.style.setProperty('left', '0px', 'important');
                sidebar.style.setProperty('position', 'relative', 'important');
                sidebar.style.setProperty('z-index', 'auto', 'important');
                
                // Force aria-expanded to true
                sidebar.setAttribute("aria-expanded", "true");
                sidebar.removeAttribute("aria-hidden");
                
                // Make sure all child elements are visible
                const sidebarChildren = sidebar.querySelectorAll('*');
                sidebarChildren.forEach(child => {
                    if (child.style.display === 'none') {
                        child.style.setProperty('display', 'block', 'important');
                    }
                    if (child.style.visibility === 'hidden') {
                        child.style.setProperty('visibility', 'visible', 'important');
                    }
                });
                
                // Hide collapse controls on desktop
                const collapseControl = window.parent.document.querySelector('[data-testid="collapsedControl"]');
                if (collapseControl) {
                    collapseControl.style.setProperty('display', 'none', 'important');
                }
                
                // Remove any Streamlit collapse classes
                sidebar.classList.remove('css-1rs6os', 'css-vk3wp9');
            }
        }
    }
    
    // Initial aggressive fix
    forceDesktopSidebarVisible();
    
    // Monitor viewport changes
    mq.addListener(forceDesktopSidebarVisible);
    
    // Very frequent checks to catch any sidebar hiding attempts
    setInterval(forceDesktopSidebarVisible, 100);
    
    // Monitor for DOM changes that might affect sidebar
    const observer = new MutationObserver(function(mutations) {
        if (!mq.matches) { // Only on desktop
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' || mutation.type === 'childList') {
                    forceDesktopSidebarVisible();
                }
            });
        }
    });
    
    // Observe the entire document for changes
    observer.observe(window.parent.document, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ['style', 'class', 'aria-expanded', 'aria-hidden']
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        setTimeout(forceDesktopSidebarVisible, 50);
        setTimeout(forceDesktopSidebarVisible, 200);
    });
    
    // Handle orientation change (mobile to desktop)
    window.addEventListener('orientationchange', function() {
        setTimeout(forceDesktopSidebarVisible, 300);
    });
}

// Start the aggressive monitor
aggressiveSidebarMonitor();

// Also ensure it runs after page loads
document.addEventListener('DOMContentLoaded', aggressiveSidebarMonitor);
setTimeout(aggressiveSidebarMonitor, 1000);
</script>
""", height=0)