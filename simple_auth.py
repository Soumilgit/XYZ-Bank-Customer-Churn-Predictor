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

def check_persistent_auth():
    if "persistent_auth_checked" not in st.session_state:
        st.session_state["persistent_auth_checked"] = True
        
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
                    const body = document.body;
                    const authDiv = document.createElement('div');
                    authDiv.id = 'auth_restore_data';
                    authDiv.style.display = 'none';
                    authDiv.setAttribute('data-name', parsed.name);
                    authDiv.setAttribute('data-email', parsed.email);
                    body.appendChild(authDiv);

                    const event = new CustomEvent('authRestore', {
                        detail: { name: parsed.name, email: parsed.email }
                    });
                    window.dispatchEvent(event);
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

def init_auth_restore():

    if "auth_init_done" not in st.session_state:
        st.session_state["auth_init_done"] = True
        
        components.html("""
        <script>
        window.addEventListener('authRestore', function(event) {
            const { name, email } = event.detail;
            
            const form = document.createElement('form');
            form.method = 'GET';
            form.action = window.location.pathname;
            
            const nameInput = document.createElement('input');
            nameInput.type = 'hidden';
            nameInput.name = 'restore_name';
            nameInput.value = name;
            
            const emailInput = document.createElement('input');
            emailInput.type = 'hidden';
            emailInput.name = 'restore_email';
            emailInput.value = email;
            
            form.appendChild(nameInput);
            form.appendChild(emailInput);
            document.body.appendChild(form);
            
            form.submit();
        });
        </script>
        <div id="auth_listener"></div>
        """, height=0)

def handle_auth_restore():

    if st.query_params.get("restore_name") and st.query_params.get("restore_email"):
        user_name = st.query_params.get("restore_name")
        user_email = st.query_params.get("restore_email")
        
        st.session_state["authenticated"] = True
        st.session_state["user"] = user_name
        st.session_state["user_email"] = user_email
        
        st.query_params.clear()
        st.rerun()
