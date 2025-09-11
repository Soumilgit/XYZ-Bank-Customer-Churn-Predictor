import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime, timedelta

def save_auth_cookie(email, name):
    """Save authentication data using a simple cookie approach"""
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    # Use JavaScript to set a cookie
    components.html(f"""
    <script>
    document.cookie = "xyz_bank_auth={json.dumps(auth_data)}; path=/; max-age=604800";
    console.log('Auth cookie set');
    </script>
    """, height=0)

def clear_auth_cookie():
    """Clear authentication cookie"""
    components.html("""
    <script>
    document.cookie = "xyz_bank_auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    console.log('Auth cookie cleared');
    </script>
    """, height=0)

def check_auth_cookie():
    """Check for authentication cookie and restore session"""
    if "cookie_checked" not in st.session_state:
        st.session_state["cookie_checked"] = True
        
        # Use JavaScript to read cookie and set session state
        components.html("""
        <script>
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
            return null;
        }
        
        const authCookie = getCookie('xyz_bank_auth');
        if (authCookie) {
            try {
                const authData = JSON.parse(authCookie);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = authData.timestamp;
                const timeDiff = currentTime - tokenTime;
                
                // Token valid for 7 days (604800 seconds)
                if (timeDiff < 604800) {
                    // Set session state by redirecting with parameters
                    const url = new URL(window.location);
                    url.searchParams.set('auto_login', 'true');
                    url.searchParams.set('user_name', authData.name);
                    url.searchParams.set('user_email', authData.email);
                    window.history.replaceState({}, '', url);
                    window.location.reload();
                } else {
                    // Token expired, clear it
                    document.cookie = "xyz_bank_auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
                }
            } catch (e) {
                console.log('Invalid auth cookie');
                document.cookie = "xyz_bank_auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
            }
        }
        </script>
        <div id="cookie_check"></div>
        """, height=0)

def handle_auto_login():
    """Handle automatic login from cookie data"""
    if st.query_params.get("auto_login") == "true":
        user_name = st.query_params.get("user_name")
        user_email = st.query_params.get("user_email")
        
        if user_name and user_email:
            # Restore session state
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_name
            st.session_state["user_email"] = user_email
            
            # Clear URL parameters
            st.query_params.clear()
            st.rerun()

def login_user(email, name):
    """Login user and save to cookie"""
    # Save to session state
    st.session_state["authenticated"] = True
    st.session_state["user"] = name
    st.session_state["user_email"] = email
    
    # Save to cookie
    save_auth_cookie(email, name)
    
    return True

def logout_user():
    """Logout user and clear cookie"""
    # Clear session state
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    
    # Clear cookie
    clear_auth_cookie()
    
    return True

def is_authenticated():
    """Check if user is currently authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user():
    """Get current authenticated user info"""
    if is_authenticated():
        return {
            "name": st.session_state.get("user"),
            "email": st.session_state.get("user_email")
        }
    return None

def init_persistent_auth():
    """Initialize persistent authentication system"""
    check_auth_cookie()
    handle_auto_login()
