"""
Auth UI
-------
Renders the login/signup gate shown before the main app.
Sets st.session_state.user to either:
  - None (not logged in yet - auth screen still showing)
  - "guest" (chose to continue without an account)
  - {"id":, "username":, "is_admin":} (logged in)
"""

import streamlit as st
import db


def require_login_or_guest():
    """Shows the login/signup screen if needed. Returns True once the user
    can proceed (either logged in or chose guest mode)."""

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is not None:
        return True

    st.title("🏛️ Government Scheme Assistant")
    st.caption("Log in to save your profile and revisit results later, or continue as a guest.")

    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Continue as Guest"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", type="primary")
            if submitted:
                user = db.verify_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create Account", type="primary")
            if submitted:
                if not new_username or not new_password:
                    st.error("Please fill in both fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 4:
                    st.error("Password should be at least 4 characters.")
                else:
                    ok, message = db.create_user(new_username, new_password)
                    if ok:
                        st.success(message + " Please log in from the Login tab.")
                    else:
                        st.error(message)

    with tab3:
        st.write("You can use the app without an account, but won't be able to save profiles for later.")
        if st.button("Continue as Guest", type="primary"):
            st.session_state.user = "guest"
            st.rerun()

    return False
