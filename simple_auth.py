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

def check_persistent_auth():
    """Check localStorage and restore authentication if valid"""
    if "persistent_auth_checked" not in st.session_state:
        st.session_state["persistent_auth_checked"] = True
        
        # Use JavaScript to check localStorage and restore session
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
                    // Use a more direct approach - modify the page content
                    const body = document.body;
                    const authDiv = document.createElement('div');
                    authDiv.id = 'auth_restore_data';
                    authDiv.style.display = 'none';
                    authDiv.setAttribute('data-name', parsed.name);
                    authDiv.setAttribute('data-email', parsed.email);
                    body.appendChild(authDiv);
                    
                    // Trigger a custom event
                    const event = new CustomEvent('authRestore', {
                        detail: { name: parsed.name, email: parsed.email }
                    });
                    window.dispatchEvent(event);
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

def init_auth_restore():
    """Initialize authentication restoration on page load"""
    # This will be called at the start of each page to check for auth restoration
    if "auth_init_done" not in st.session_state:
        st.session_state["auth_init_done"] = True
        
        # Add a JavaScript listener for auth restoration
        components.html("""
        <script>
        window.addEventListener('authRestore', function(event) {
            const { name, email } = event.detail;
            
            // Create a form to submit the auth data
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
            
            // Submit the form
            form.submit();
        });
        </script>
        <div id="auth_listener"></div>
        """, height=0)

def handle_auth_restore():
    """Handle authentication restoration from URL parameters"""
    if st.query_params.get("restore_name") and st.query_params.get("restore_email"):
        user_name = st.query_params.get("restore_name")
        user_email = st.query_params.get("restore_email")
        
        # Restore session state
        st.session_state["authenticated"] = True
        st.session_state["user"] = user_name
        st.session_state["user_email"] = user_email
        
        # Clear URL parameters
        st.query_params.clear()
        st.rerun()
