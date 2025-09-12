import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def save_auth_to_storage(email, name):
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }

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

def check_persistent_auth():
    """Check if user is authenticated via persistent storage and restore session"""
    if "persistent_auth_checked" not in st.session_state:
        st.session_state["persistent_auth_checked"] = True
        
        auth_data = components.html("""
        <script>
        const authData = localStorage.getItem('xyz_bank_auth');
        if (authData) {
            try {
                const parsed = JSON.parse(authData);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = parsed.timestamp;
                const timeDiff = currentTime - tokenTime;
                
                if (timeDiff < 604800) {
                    // Create a form to submit auth data
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = window.location.href;
                    
                    const nameInput = document.createElement('input');
                    nameInput.type = 'hidden';
                    nameInput.name = 'restored_user_name';
                    nameInput.value = parsed.name;
                    
                    const emailInput = document.createElement('input');
                    emailInput.type = 'hidden';
                    emailInput.name = 'restored_user_email';
                    emailInput.value = parsed.email;
                    
                    form.appendChild(nameInput);
                    form.appendChild(emailInput);
                    document.body.appendChild(form);
                    
                    form.submit();
                } else {
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

def handle_auth_restore():
    if st.query_params.get("auth_restore") == "true":
        user_name = st.query_params.get("user_name")
        user_email = st.query_params.get("user_email")
        
        if user_name and user_email:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_name
            st.session_state["user_email"] = user_email

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
