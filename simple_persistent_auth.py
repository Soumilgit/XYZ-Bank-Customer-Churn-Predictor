import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime, timedelta

def save_auth_to_storage(email, name):
    """Save authentication data using a simple approach"""
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    # Store in session state for persistence
    st.session_state["persistent_auth"] = auth_data
    
    # Also try to save to browser storage
    components.html(f"""
    <script>
    try {{
        localStorage.setItem('xyz_bank_auth', JSON.stringify({json.dumps(auth_data)}));
        console.log('Auth data saved to localStorage');
    }} catch (e) {{
        console.log('localStorage not available');
    }}
    </script>
    """, height=0)

def clear_auth_from_storage():
    """Clear authentication data"""
    # Clear from session state
    if "persistent_auth" in st.session_state:
        del st.session_state["persistent_auth"]
    
    # Clear from browser storage
    components.html("""
    <script>
    try {
        localStorage.removeItem('xyz_bank_auth');
        console.log('Auth data cleared from localStorage');
    } catch (e) {
        console.log('localStorage not available');
    }
    </script>
    """, height=0)

def check_and_restore_auth():
    """Check for stored authentication and restore if valid"""
    if "auth_restore_attempted" not in st.session_state:
        st.session_state["auth_restore_attempted"] = True
        
        # First check session state
        if "persistent_auth" in st.session_state:
            auth_data = st.session_state["persistent_auth"]
            current_time = int(datetime.now().timestamp())
            token_time = auth_data.get("timestamp", 0)
            time_diff = current_time - token_time
            
            # Token valid for 7 days (604800 seconds)
            if time_diff < 604800:
                st.session_state["authenticated"] = True
                st.session_state["user"] = auth_data["name"]
                st.session_state["user_email"] = auth_data["email"]
                return True
            else:
                # Token expired, clear it
                del st.session_state["persistent_auth"]
        
        # If not in session state, try to restore from browser storage
        components.html("""
        <script>
        try {
            const authData = localStorage.getItem('xyz_bank_auth');
            if (authData) {
                const parsed = JSON.parse(authData);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = parsed.timestamp;
                const timeDiff = currentTime - tokenTime;
                
                // Token valid for 7 days (604800 seconds)
                if (timeDiff < 604800) {
                    // Redirect with auth data to restore session
                    const url = new URL(window.location);
                    url.searchParams.set('restore_auth', 'true');
                    url.searchParams.set('user_name', parsed.name);
                    url.searchParams.set('user_email', parsed.email);
                    window.history.replaceState({}, '', url);
                    window.location.reload();
                } else {
                    // Token expired, clear it
                    localStorage.removeItem('xyz_bank_auth');
                }
            }
        } catch (e) {
            console.log('Error checking localStorage:', e);
        }
        </script>
        <div id="auth_restore"></div>
        """, height=0)
    
    return False

def handle_auth_restore():
    """Handle authentication restoration from URL parameters"""
    if st.query_params.get("restore_auth") == "true":
        user_name = st.query_params.get("user_name")
        user_email = st.query_params.get("user_email")
        
        if user_name and user_email:
            # Restore session state
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_name
            st.session_state["user_email"] = user_email
            
            # Save to persistent storage
            save_auth_to_storage(user_email, user_name)
            
            # Clear URL parameters
            st.query_params.clear()
            st.rerun()

def login_user(email, name):
    """Login user and save to persistent storage"""
    # Save to session state
    st.session_state["authenticated"] = True
    st.session_state["user"] = name
    st.session_state["user_email"] = email
    
    # Save to persistent storage
    save_auth_to_storage(email, name)
    
    return True

def logout_user():
    """Logout user and clear persistent storage"""
    # Clear session state
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    
    # Clear persistent storage
    clear_auth_from_storage()
    
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
    # Try to restore from session state first
    if check_and_restore_auth():
        return
    
    # Handle restoration from URL parameters
    handle_auth_restore()
