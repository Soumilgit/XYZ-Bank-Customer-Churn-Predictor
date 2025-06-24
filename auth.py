import streamlit as st
import hashlib
import sqlite3
import requests
import re

import utils as ut
ut.apply_sidebar_styles()

# --- SECRETS FROM .streamlit/secrets.toml ---
EMAILJS_SERVICE_ID = st.secrets["EMAILJS_SERVICE_ID"]
EMAILJS_TEMPLATE_ID = st.secrets["EMAILJS_TEMPLATE_ID"]
EMAILJS_PUBLIC_KEY = st.secrets["EMAILJS_PUBLIC_KEY"]

# --- INIT DB ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- PASSWORD HASHING ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- PASSWORD VALIDATION ---
def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$"
    return re.match(pattern, password)

# --- DB HELPERS ---
def user_exists(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def update_password(email, new_password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE email=?", (hash_password(new_password), email))
    conn.commit()
    conn.close()

def add_user(email, name, password_hash):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (email, name, password_hash))
    conn.commit()
    conn.close()

def verify_login(email, password):
    user = user_exists(email)
    if user and user[2] == hash_password(password):
        return True, user[1]
    return False, None

# --- EMAILJS FUNCTIONS ---
def send_welcome_email(name, email):
    try:
        payload = {
            "service_id": EMAILJS_SERVICE_ID,
            "template_id": EMAILJS_TEMPLATE_ID,
            "user_id": EMAILJS_PUBLIC_KEY,
            "template_params": {
                "to_name": name,
                "to_email": email,
                "user_name": name
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Welcome email sent!")
    except Exception as e:
        print(f"⚠️ Email error: {e}")

def send_reset_email(email):
    try:
        payload = {
            "service_id": EMAILJS_SERVICE_ID,
            "template_id": EMAILJS_TEMPLATE_ID,
            "user_id": EMAILJS_PUBLIC_KEY,
            "template_params": {
                "to_name": "User",
                "to_email": email,
                "user_name": "User"
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Reset email sent!")
    except Exception as e:
        print(f"⚠️ Email error: {e}")

# --- REGISTER USER ---
def register_user(email, name, password):
    if user_exists(email):
        return False, "Email already exists."

    if not is_valid_password(password):
        return False, "Password must be ≥8 characters, include upper/lowercase, digit & symbol."

    add_user(email, name, hash_password(password))
    send_welcome_email(name, email)
    return True, "Registration successful!"

# --- RESET PASSWORD ---
def forgot_password_flow():
    st.subheader("🔁 Forgot Password?")
    email = st.text_input("Enter your registered email", key="forgot_email")
    new_pass = st.text_input("Enter new password", type="password", key="new_pass")
    confirm_pass = st.text_input("Confirm new password", type="password", key="confirm_pass")

    if st.button("Reset Password"):
        user = user_exists(email)
        if not user:
            st.error("Email not found.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif not is_valid_password(new_pass):
            st.error("Password must be ≥8 characters, include upper/lowercase, digit & symbol.")
        else:
            update_password(email, new_pass)
            send_reset_email(email)
            st.success("✅ Password reset successful!")

# --- LOGIN/SIGNUP UI ---
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
                st.session_state["authenticated"] = True
                st.session_state["user"] = name
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

# --- LOGOUT ---

# --- MAIN ---
def main():
    init_db()
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        # Green success message (stays)
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


        # Red alert with zoom animation, shown once
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
                0% {
                    opacity: 0;
                    transform: scale(0.8);
                }
                100% {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            </style>
            """, unsafe_allow_html=True)

    else:
        login_signup_interface()

