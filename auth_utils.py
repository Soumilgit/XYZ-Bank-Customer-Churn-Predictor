import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

def save_auth_to_storage(email, name):
    """Save authentication data to browser localStorage"""
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    # Use JavaScript to save to localStorage
    components.html(f"""
    <script>
    localStorage.setItem('xyz_bank_auth', JSON.stringify({json.dumps(auth_data)}));
    console.log('Auth data saved to localStorage');
    </script>
    """, height=0)

def clear_auth_from_storage():
    """Clear authentication data from browser localStorage"""
    components.html("""
    <script>
    localStorage.removeItem('xyz_bank_auth');
    console.log('Auth data cleared from localStorage');
    </script>
    """, height=0)

def check_and_restore_auth():
    """Check localStorage and restore authentication if valid"""
    if "auth_restore_checked" not in st.session_state:
        st.session_state["auth_restore_checked"] = True
        
        # Use JavaScript to check localStorage and set a flag
        components.html("""
        <script>
        const authData = localStorage.getItem('xyz_bank_auth');
        if (authData) {
            try {
                const parsed = JSON.parse(authData);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = parsed.timestamp;
                const timeDiff = currentTime - tokenTime;
                
                // Token valid for 7 days (604800 seconds)
                if (timeDiff < 604800) {
                    // Set a flag in session storage to indicate auth should be restored
                    sessionStorage.setItem('restore_auth', 'true');
                    sessionStorage.setItem('restore_name', parsed.name);
                    sessionStorage.setItem('restore_email', parsed.email);
                    
                    // Reload the page to trigger auth restoration
                    window.location.reload();
                } else {
                    // Token expired, clear it
                    localStorage.removeItem('xyz_bank_auth');
                }
            } catch (e) {
                console.log('Invalid auth data in localStorage');
                localStorage.removeItem('xyz_bank_auth');
            }
        }
        </script>
        <div id="auth_check"></div>
        """, height=0)

def restore_auth_from_session():
    """Restore authentication from session storage"""
    if "auth_restored" not in st.session_state:
        st.session_state["auth_restored"] = True
        
        # Check if we need to restore auth
        components.html("""
        <script>
        const shouldRestore = sessionStorage.getItem('restore_auth');
        if (shouldRestore === 'true') {
            const name = sessionStorage.getItem('restore_name');
            const email = sessionStorage.getItem('restore_email');
            
            if (name && email) {
                // Set session state via URL parameters
                const url = new URL(window.location);
                url.searchParams.set('restore_auth', 'true');
                url.searchParams.set('restore_name', name);
                url.searchParams.set('restore_email', email);
                window.history.replaceState({}, '', url);
                
                // Clear session storage
                sessionStorage.removeItem('restore_auth');
                sessionStorage.removeItem('restore_name');
                sessionStorage.removeItem('restore_email');
                
                // Reload to apply changes
                window.location.reload();
            }
        }
        </script>
        <div id="restore_check"></div>
        """, height=0)

def handle_auth_restore():
    """Handle authentication restoration from URL parameters"""
    if st.query_params.get("restore_auth") == "true":
        user_name = st.query_params.get("restore_name")
        user_email = st.query_params.get("restore_email")
        
        if user_name and user_email:
            # Restore session state
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_name
            st.session_state["user_email"] = user_email
            
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
