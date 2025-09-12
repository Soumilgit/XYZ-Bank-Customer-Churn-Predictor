import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

def save_auth_cookie(email, name):
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    components.html(f"""
    <script>
    document.cookie = "xyz_bank_auth={json.dumps(auth_data)}; path=/; max-age=604800";
    console.log('Auth cookie set');
    </script>
    """, height=0)

def clear_auth_cookie():
    components.html("""
    <script>
    document.cookie = "xyz_bank_auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    console.log('Auth cookie cleared');
    </script>
    """, height=0)

def check_auth_cookie():
    if "cookie_checked" not in st.session_state:
        st.session_state["cookie_checked"] = True
        
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
                
                if (timeDiff < 604800) {
                    // Set session state by redirecting with parameters
                    const url = new URL(window.location);
                    url.searchParams.set('auto_login', 'true');
                    url.searchParams.set('user_name', authData.name);
                    url.searchParams.set('user_email', authData.email);
                    window.history.replaceState({}, '', url);
                    window.location.reload();
                } else {
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
    if st.query_params.get("auto_login") == "true":
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
    
    save_auth_cookie(email, name)
    
    return True

def logout_user():

    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    
    clear_auth_cookie()
    
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

    check_auth_cookie()
    handle_auto_login()
