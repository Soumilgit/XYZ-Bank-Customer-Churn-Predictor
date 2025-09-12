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
    
    components.html(f"""
    <script>
    localStorage.setItem('xyz_bank_auth', JSON.stringify({json.dumps(auth_data)}));
    console.log('Auth data saved to localStorage');
    </script>
    """, height=0)

def clear_auth_from_storage():
    components.html("""
    <script>
    localStorage.removeItem('xyz_bank_auth');
    console.log('Auth data cleared from localStorage');
    </script>
    """, height=0)

def check_and_restore_auth():
    if "auth_restore_checked" not in st.session_state:
        st.session_state["auth_restore_checked"] = True
    
        components.html("""
        <script>
        const authData = localStorage.getItem('xyz_bank_auth');
        if (authData) {
            try {
                const parsed = JSON.parse(authData);
                const currentTime = Math.floor(Date.now() / 1000);
                const tokenTime = parsed.timestamp;
                const timeDiff = currentTime - tokenTime;
                if (timeDiff < 604800) {
                    sessionStorage.setItem('restore_auth', 'true');
                    sessionStorage.setItem('restore_name', parsed.name);
                    sessionStorage.setItem('restore_email', parsed.email);
                    
                    window.location.reload();
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

def restore_auth_from_session():
    if "auth_restored" not in st.session_state:
        st.session_state["auth_restored"] = True

        components.html("""
        <script>
        const shouldRestore = sessionStorage.getItem('restore_auth');
        if (shouldRestore === 'true') {
            const name = sessionStorage.getItem('restore_name');
            const email = sessionStorage.getItem('restore_email');
            
            if (name && email) {
                const url = new URL(window.location);
                url.searchParams.set('restore_auth', 'true');
                url.searchParams.set('restore_name', name);
                url.searchParams.set('restore_email', email);
                window.history.replaceState({}, '', url);
    
                sessionStorage.removeItem('restore_auth');
                sessionStorage.removeItem('restore_name');
                sessionStorage.removeItem('restore_email');
                
                window.location.reload();
            }
        }
        </script>
        <div id="restore_check"></div>
        """, height=0)

def handle_auth_restore():
    if st.query_params.get("restore_auth") == "true":
        user_name = st.query_params.get("restore_name")
        user_email = st.query_params.get("restore_email")
        
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
