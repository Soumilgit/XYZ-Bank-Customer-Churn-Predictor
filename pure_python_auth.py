import streamlit as st
import json
import os
from datetime import datetime, timedelta

# File to store auth data
AUTH_FILE = "auth_data.json"

def save_auth_to_file(email, name):
    """Save authentication data to a local file"""
    auth_data = {
        "email": email,
        "name": name,
        "timestamp": int(datetime.now().timestamp())
    }
    
    try:
        with open(AUTH_FILE, 'w') as f:
            json.dump(auth_data, f)
        return True
    except Exception as e:
        st.error(f"Error saving auth data: {e}")
        return False

def load_auth_from_file():
    """Load authentication data from file"""
    try:
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'r') as f:
                auth_data = json.load(f)
            return auth_data
    except Exception as e:
        st.error(f"Error loading auth data: {e}")
    return None

def clear_auth_file():
    """Clear authentication file"""
    try:
        if os.path.exists(AUTH_FILE):
            os.remove(AUTH_FILE)
        return True
    except Exception as e:
        st.error(f"Error clearing auth data: {e}")
        return False

def is_auth_valid(auth_data):
    """Check if authentication data is still valid"""
    if not auth_data:
        return False
    
    current_time = int(datetime.now().timestamp())
    token_time = auth_data.get("timestamp", 0)
    time_diff = current_time - token_time
    
    # Token valid for 7 days (604800 seconds)
    return time_diff < 604800

def check_and_restore_auth():
    """Check for stored authentication and restore if valid"""
    if "auth_restore_attempted" not in st.session_state:
        st.session_state["auth_restore_attempted"] = True
        
        # Load auth data from file
        auth_data = load_auth_from_file()
        
        if auth_data and is_auth_valid(auth_data):
            # Restore session state
            st.session_state["authenticated"] = True
            st.session_state["user"] = auth_data["name"]
            st.session_state["user_email"] = auth_data["email"]
            return True
        elif auth_data:
            # Token expired, clear it
            clear_auth_file()
    
    return False

def login_user(email, name):
    """Login user and save to file"""
    # Save to session state
    st.session_state["authenticated"] = True
    st.session_state["user"] = name
    st.session_state["user_email"] = email
    
    # Save to file
    save_auth_to_file(email, name)
    
    return True

def logout_user():
    """Logout user and clear file"""
    # Clear session state
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    
    # Clear file
    clear_auth_file()
    
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
    check_and_restore_auth()
