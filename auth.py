import streamlit as st
import hashlib
import requests
import re
from datetime import datetime
from supabase import create_client
import pure_python_auth as ppa

import utils as ut
ut.apply_sidebar_styles()

# Supabase Init
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# EmailJS Secrets
EMAILJS_SERVICE_ID = st.secrets["EMAILJS_SERVICE_ID"]
EMAILJS_TEMPLATE_ID = st.secrets["EMAILJS_TEMPLATE_ID"]
EMAILJS_PUBLIC_KEY = st.secrets["EMAILJS_PUBLIC_KEY"]

# PASSWORD UTILS
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$"
    return re.match(pattern, password)

# DB HELPERS via Supabase
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
    hashed = hash_password(password)
    result = supabase.table("users").select("*").eq("email", email).eq("password", hashed).execute()
    if result.data:
        return True, result.data[0]["name"]
    return False, None

# EMAILJS FUNCTION
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

# REGISTER USER
def register_user(email, name, password):
    if user_exists(email):
        return False, "Email already exists."
    if not is_valid_password(password):
        return False, "Password must be ≥8 characters, include upper/lowercase, digit & symbol."

    add_user(email, name, hash_password(password))
    send_welcome_email(name, email)
    return True, "Registration successful!"

# RESET PASSWORD
def forgot_password_flow():
    st.subheader("🔁 Forgot Password?")
    email = st.text_input("Enter your registered email", key="forgot_email")
    new_pass = st.text_input("Enter new password", type="password", key="new_pass")
    confirm_pass = st.text_input("Confirm new password", type="password", key="confirm_pass")

    if st.button("Reset Password"):
        if not user_exists(email):
            st.error("Email not found.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif not is_valid_password(new_pass):
            st.error("Password must be ≥8 characters, include upper/lowercase, digit & symbol.")
        else:
            update_password(email, hash_password(new_pass))
            send_reset_email(email)
            st.success("✅ Password reset successful!")

# LOGIN/SIGNUP UI
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
                # Use persistent authentication
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

# MAIN ENTRY
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
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
            🔓 Logged in as {st.session_state['user']}
        </div>
        """, unsafe_allow_html=True)

        if "post_login_hint_shown" not in st.session_state:
            st.session_state["post_login_hint_shown"] = True
            st.markdown("""
            <div class="zoom-box-login">
                🚀 <strong>Use '≫', top-left, to access dashboard/logout.</strong>
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
