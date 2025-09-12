import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

def save_auth_to_storage(email, name):
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    st.session_state["persistent_auth"] = auth_data
    
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

    if "persistent_auth" in st.session_state:
        del st.session_state["persistent_auth"]
    
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
        
        if "persistent_auth" in st.session_state:
            auth_data = st.session_state["persistent_auth"]
            current_time = int(datetime.now().timestamp())
            token_time = auth_data.get("timestamp", 0)
            time_diff = current_time - token_time
            
            if time_diff < 604800:
                st.session_state["authenticated"] = True
                st.session_state["user"] = auth_data["name"]
                st.session_state["user_email"] = auth_data["email"]
                return True
            else:
                del st.session_state["persistent_auth"]
        
        components.html("""
        <script>
        try {
            const authData = localStorage.getItem('xyz_bank_auth');
            if (authData) {
                const parsed = JSON.parse(authData);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = parsed.timestamp;
                const timeDiff = currentTime - tokenTime;
                
                if (timeDiff < 604800) {
                    // Redirect with auth data to restore session
                    const url = new URL(window.location);
                    url.searchParams.set('restore_auth', 'true');
                    url.searchParams.set('user_name', parsed.name);
                    url.searchParams.set('user_email', parsed.email);
                    window.history.replaceState({}, '', url);
                    window.location.reload();
                } else {
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

    if st.query_params.get("restore_auth") == "true":
        user_name = st.query_params.get("user_name")
        user_email = st.query_params.get("user_email")
        
        if user_name and user_email:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_name
            st.session_state["user_email"] = user_email
            
            save_auth_to_storage(user_email, user_name)
            
            st.query_params.clear()
            st.rerun()

def login_user(email, name):

    st.session_state["authenticated"] = True
    st.session_state["user"] = name
    st.session_state["user_email"] = email
    
    save_auth_to_storage(email, name)
    
    return True

def logout_user():

    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    
    clear_auth_from_storage()
    
    return True

def is_authenticated():

    return st.session_state.get("authenticated", False)

def get_current_user():

    if is_authenticated():
        return {
            "name": st.session_state.get("user"),
            "email": st.session_state.get("user_email")
        }
    return None

def init_persistent_auth():

    if check_and_restore_auth():
        return

    handle_auth_restore()
