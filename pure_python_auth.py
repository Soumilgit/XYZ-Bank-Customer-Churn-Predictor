import streamlit as st
import json
import os
from datetime import datetime

AUTH_FILE = "auth_data.json"

def save_auth_to_file(email, name):
 
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

    try:
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'r') as f:
                auth_data = json.load(f)
            return auth_data
    except Exception as e:
        st.error(f"Error loading auth data: {e}")
    return None

def clear_auth_file():

    try:
        if os.path.exists(AUTH_FILE):
            os.remove(AUTH_FILE)
        return True
    except Exception as e:
        st.error(f"Error clearing auth data: {e}")
        return False

def is_auth_valid(auth_data):

    if not auth_data:
        return False
    
    current_time = int(datetime.now().timestamp())
    token_time = auth_data.get("timestamp", 0)
    time_diff = current_time - token_time

    return time_diff < 604800

def check_and_restore_auth():

    if "auth_restore_attempted" not in st.session_state:
        st.session_state["auth_restore_attempted"] = True

        auth_data = load_auth_from_file()
        
        if auth_data and is_auth_valid(auth_data):
            st.session_state["authenticated"] = True
            st.session_state["user"] = auth_data["name"]
            st.session_state["user_email"] = auth_data["email"]
            return True
        elif auth_data:
            clear_auth_file()
    
    return False

def login_user(email, name):

    st.session_state["authenticated"] = True
    st.session_state["user"] = name
    st.session_state["user_email"] = email
    st.session_state["reset_sidebar_on_login"] = True  # Flag to reset sidebar state

    save_auth_to_file(email, name)
    
    return True

def logout_user():
 
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["user_email"] = None
    st.session_state["force_sidebar_collapse"] = True

    clear_auth_file()
    
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
    check_and_restore_auth()
