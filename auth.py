import streamlit as st
import hashlib
import requests
import re
import html
from datetime import datetime
from supabase import create_client
import pure_python_auth as ppa
try:
    import bcrypt
except ImportError:
    bcrypt = None

import utils as ut
ut.apply_sidebar_styles()

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

EMAILJS_SERVICE_ID = st.secrets["EMAILJS_SERVICE_ID"]
EMAILJS_TEMPLATE_ID = st.secrets["EMAILJS_TEMPLATE_ID"]
EMAILJS_PUBLIC_KEY = st.secrets["EMAILJS_PUBLIC_KEY"]

def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) and len(email) <= 254

def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$"
    return re.match(pattern, password)

def sanitize_name(name):
    """Sanitize and validate name input to prevent XSS"""
    if not name:
        return None, "Name is required"
    
    # Escape HTML characters to prevent XSS
    safe_name = html.escape(name.strip())
    
    # Length check
    if len(safe_name) > 100:
        return None, "Name too long (max 100 characters)"
    
    # Character validation (letters, spaces, hyphens, apostrophes, dots)
    if not re.match(r"^[a-zA-Z\s\-\'\.]+$", safe_name):
        return None, "Name contains invalid characters (only letters, spaces, hyphens, apostrophes allowed)"
    
    return safe_name, None

def user_exists(email):
    result = supabase.table("users").select("email").eq("email", email).execute()
    return bool(result.data)

def add_user(email, name, password_hash):
    return supabase.table("users").insert({
        "email": email,
        "name": name,
        "password": password_hash
    }).execute()

def update_password(email, new_password_hash):
    return supabase.table("users").update({
        "password": new_password_hash
    }).eq("email", email).execute()

def verify_login(email, password):
    result = supabase.table("users").select("*").eq("email", email).execute()
    if not result.data:
        return False, None

    user_row = result.data[0]
    stored_hash = user_row.get("password", "")
    user_name = user_row.get("name")

    if bcrypt and isinstance(stored_hash, str) and stored_hash.startswith("$2"):
        try:
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                return True, user_name
        except ValueError:
            pass

    sha_hash = hashlib.sha256(password.encode()).hexdigest()
    if stored_hash == sha_hash:
        if bcrypt:
            try:
                new_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                update_password(email, new_hash)
            except Exception:
                pass
        return True, user_name

    return False, None

def send_email(title, name, email, message):
    try:
        payload = {
            "service_id": EMAILJS_SERVICE_ID,
            "template_id": EMAILJS_TEMPLATE_ID,
            "user_id": EMAILJS_PUBLIC_KEY,  
            "template_params": {
                "title": title,
                "name": name,
                "message": message,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, headers=headers)
        print("✅ EmailJS:", response.status_code, response.text)
    except Exception as e:
        print(f"⚠️ Email error: {e}")


def send_welcome_email(name, email):
    send_email(
        title="Welcome to XYZ Bank",
        name=name,
        email=email,
        message=f"New user registered: {name} ({email})"
    )

def send_reset_email(email):
    send_email(
        title="Password Reset Request",
        name="User",
        email=email,
        message=f"Password reset request for: {email}"
    )

def register_user(email, name, password):
    # Validate email
    if not is_valid_email(email):
        return False, "Invalid email format."
    
    if user_exists(email):
        return False, "Email already exists."
    
    # Sanitize name (XSS protection)
    safe_name, name_error = sanitize_name(name)
    if name_error:
        return False, name_error
    
    if not is_valid_password(password):
        return False, "Password must be ≥8 characters, include upper/lowercase, digit & symbol."

    add_user(email, safe_name, hash_password(password))
    send_welcome_email(safe_name, email)
    return True, "Registration successful!"

def forgot_password_flow():
    st.subheader("🔁 Forgot Password?")
    email = st.text_input("Enter your registered email", key="forgot_email")
    new_pass = st.text_input("Enter new password", type="password", key="new_pass")
    confirm_pass = st.text_input("Confirm new password", type="password", key="confirm_pass")

    if st.button("Reset Password"):
        if not is_valid_email(email):
            st.error("Invalid email format.")
        elif not user_exists(email):
            st.error("Email not found.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif not is_valid_password(new_pass):
            st.error("Password must be ≥8 characters, include upper/lowercase, digit & symbol.")
        else:
            update_password(email, hash_password(new_pass))
            send_reset_email(email)
            st.success("✅ Password reset successful!")

def login_signup_interface():
    st.markdown("## 🔐 Login or Sign Up")
    tabs = st.tabs(["Login", "Sign Up", "Forgot Password?"])

    with tabs[0]:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, name = verify_login(email, password)
            if success:
                ppa.login_user(email, name)
                st.success(f"Welcome back, {name}!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tabs[1]:
        st.subheader("Sign Up")
        name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        st.caption("Password must be ≥8 chars, include upper/lowercase, digit & symbol.")
        if st.button("Register"):
            ok, msg = register_user(email, name, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    with tabs[2]:
        forgot_password_flow()

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        # Sanitize username to prevent XSS
        safe_username = html.escape(st.session_state.get('user', 'Unknown'))
        
        st.markdown(f"""
        <div style="
            color: #155724;
            background-color: #d4edda;
            border-left: 6px solid #c3e6cb;
            padding: 14px 20px;
            border-radius: 6px;
            font-size: 26px;
            margin-bottom: 12px;
            font-weight: 500;">
            🔓 Logged in as {safe_username}
        </div>
        """, unsafe_allow_html=True)

        if "post_login_hint_shown" not in st.session_state:
            st.session_state["post_login_hint_shown"] = True
            st.markdown("""
            <div class="zoom-box-login">
                🚀 <strong>Tap '>>' to access sidebar on mobile.</strong>
            </div>
            <style>
            .zoom-box-login {
                background-color: #f8d7da;
                color: #721c24;
                padding: 14px 20px;
                border-radius: 6px;
                font-size: 26px;
                border-left: 6px solid #f5c6cb;
                margin-top: 10px;
                margin-bottom: 24px;
                animation: zoomIn 0.6s ease;
            }
            @keyframes zoomIn {
                0% {opacity: 0; transform: scale(0.8);}
                100% {opacity: 1; transform: scale(1);}
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        login_signup_interface()
