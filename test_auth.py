#!/usr/bin/env python3

import streamlit as st
import simple_auth as sa

def test_auth_functions():
    """Test the authentication functions"""
    st.title("Authentication Test")
    
    # Test 1: Check if user is authenticated
    st.subheader("Test 1: Authentication Status")
    is_auth = sa.is_authenticated()
    st.write(f"User authenticated: {is_auth}")
    
    # Test 2: Get current user
    st.subheader("Test 2: Current User")
    user = sa.get_current_user()
    st.write(f"Current user: {user}")
    
    # Test 3: Login simulation
    st.subheader("Test 3: Login Simulation")
    if st.button("Simulate Login"):
        sa.login_user("test@example.com", "Test User")
        st.success("Login simulated!")
        st.rerun()
    
    # Test 4: Logout simulation
    st.subheader("Test 4: Logout Simulation")
    if st.button("Simulate Logout"):
        sa.logout_user()
        st.success("Logout simulated!")
        st.rerun()
    
    # Test 5: Persistent storage test
    st.subheader("Test 5: Persistent Storage")
    if st.button("Save to Storage"):
        sa.save_auth_to_storage("test@example.com", "Test User")
        st.success("Data saved to localStorage!")
    
    if st.button("Clear Storage"):
        sa.clear_auth_from_storage()
        st.success("Data cleared from localStorage!")
    
    # Test 6: Check persistent auth
    st.subheader("Test 6: Check Persistent Auth")
    if st.button("Check Persistent Auth"):
        sa.check_persistent_auth()
        st.success("Persistent auth check completed!")

if __name__ == "__main__":
    test_auth_functions()
