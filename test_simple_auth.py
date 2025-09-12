#!/usr/bin/env python3

import streamlit as st
import simple_persistent_auth as spa

st.set_page_config(
    page_title="Auth Test",
    page_icon="🔐",
    layout="centered"
)

spa.init_persistent_auth()

st.title("🔐 Simple Auth Test")

st.subheader("Current Status")
is_auth = spa.is_authenticated()
user = spa.get_current_user()

if is_auth:
    st.success(f"✅ Logged in as: {user['name']} ({user['email']})")
else:
    st.warning("❌ Not logged in")

st.subheader("Test Controls")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 Login", use_container_width=True):
        spa.login_user("test@example.com", "Test User")
        st.success("Logged in! Check if it persists after refresh.")
        st.rerun()

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        spa.logout_user()
        st.success("Logged out!")
        st.rerun()

st.subheader("Instructions")
st.markdown("""
1. Click "Login" to log in
2. Refresh the page (F5 or Ctrl+R)
3. You should still be logged in
4. Click "Logout" to log out
5. Refresh again - you should be logged out
""")

st.subheader("Debug Info")
st.write("Session State:", dict(st.session_state))
