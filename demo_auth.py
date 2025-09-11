#!/usr/bin/env python3
"""
Demo script showing persistent authentication in action
"""

import streamlit as st
import simple_auth as sa

# Page config
st.set_page_config(
    page_title="Auth Demo",
    page_icon="🔐",
    layout="centered"
)

# Initialize authentication
sa.init_auth_restore()
sa.check_persistent_auth()
sa.handle_auth_restore()

st.title("🔐 Persistent Authentication Demo")
st.markdown("This demo shows how persistent authentication works in your Streamlit app.")

# Show current authentication status
st.subheader("Current Status")
is_auth = sa.is_authenticated()
user = sa.get_current_user()

if is_auth:
    st.success(f"✅ Logged in as: {user['name']} ({user['email']})")
else:
    st.warning("❌ Not logged in")

# Demo controls
st.subheader("Demo Controls")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 Simulate Login", use_container_width=True):
        sa.login_user("demo@example.com", "Demo User")
        st.success("Login successful! Refresh the page to test persistence.")
        st.rerun()

with col2:
    if st.button("🚪 Simulate Logout", use_container_width=True):
        sa.logout_user()
        st.success("Logout successful! Refresh the page to test.")
        st.rerun()

# Instructions
st.subheader("How to Test Persistent Authentication")

st.markdown("""
1. **Click "Simulate Login"** - This will log you in and save data to localStorage
2. **Refresh the page** - The authentication should persist automatically
3. **Click "Simulate Logout"** - This will clear the authentication
4. **Refresh the page** - You should be logged out

### What happens behind the scenes:
- Login data is saved to browser localStorage
- On page refresh, JavaScript checks localStorage for valid auth data
- If valid data exists, the session is automatically restored
- If data is expired (>7 days), it's automatically cleared
""")

# Show localStorage data (for debugging)
st.subheader("Debug Info")
st.markdown("""
**To see localStorage data:**
1. Open browser developer tools (F12)
2. Go to Application/Storage tab
3. Look for `xyz_bank_auth` in localStorage
4. Check the console for authentication logs
""")

# Footer
st.markdown("---")
st.markdown("**Note:** This is a demo. In your actual app, authentication is handled through the Supabase database.")
