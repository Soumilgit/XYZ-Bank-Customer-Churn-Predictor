# Homepage.py
import streamlit as st
import base64



st.set_page_config(
    page_title="XYZ Bank Analytics",
    layout="centered"
)
import utils as ut
ut.apply_sidebar_styles()

def add_header_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{encoded_string}" style="max-height: 200px;">
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Homepage content UI only (no sidebar logic here!)
    st.markdown(
        """
        <style>
        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .title {
            font-size: 2.5rem;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
        }
        .feature-title {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            color: #7f8c8d;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 1rem;
            margin: 1rem 0;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.3s;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .stButton>button:disabled {
    background-color: #6c4db0 !important; /* reddish-blue */
    color: #f8f9fa !important;
    border: none !important;
    cursor: not-allowed !important;
    opacity: 1 !important; /* override faded look */
    font-weight: 600;
    border-radius: 4px;
}

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("""<div style="text-align: center; margin-bottom: 2rem;"><h1>XYZ Bank</h1></div>""", unsafe_allow_html=True)

        try:
            add_header_image('background.png')
        except:
            st.markdown("""<div style="text-align: center; margin-bottom: 2rem;"><h1>XYZ Bank</h1></div>""", unsafe_allow_html=True)

        st.markdown('<h1 class="title">Customer Analytics Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Advanced tools to understand and retain your customers</p>', unsafe_allow_html=True)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Churn Prediction</div>
                        <div class="feature-desc">Identify customers at risk of leaving with our machine learning models.</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Customer Insights</div>
                        <div class="feature-desc">Understand customer behavior patterns and preferences.</div>
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Retention Strategies</div>
                        <div class="feature-desc">Get personalized recommendations to improve customer loyalty.</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Performance Metrics</div>
                        <div class="feature-desc">Track key indicators of customer satisfaction and engagement.</div>
                    </div>
                    """, unsafe_allow_html=True)

        is_authenticated = st.session_state.get("authenticated", False)

        if is_authenticated:
            if st.button("Launch Churn Prediction Tool", key="churn_button"):
                st.session_state.page = "Dashboard"
                st.rerun()
        else:
                st.button("🔒 Please log in to access Churn Tool", disabled=True)


    st.markdown("""
    <style>
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    </style>
    <div class="footer">
        <p>© 2025 XYZ Bank Analytics | Secure Banking Platform</p>
    </div>
    """, unsafe_allow_html=True)
