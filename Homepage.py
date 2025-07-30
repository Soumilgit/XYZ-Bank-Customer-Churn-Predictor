import streamlit as st
import base64

def apply_sidebar_styles():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] li a {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            margin: 0.4rem 0 !important;
            font-size: 16px !important;
            width: 100% !important;
            border: none !important;
            display: block !important;
            text-align: center !important;
        }
        [data-testid="stSidebarNav"] li a:hover {
            background-color: #0056b3 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
    apply_sidebar_styles()

    st.markdown(
        """
        <style>
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem;
            border-radius: 15px;
            background-color: #ffffff;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }
        .title {
            font-size: 2.2rem !important;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
        }
        .subtitle {
            font-size: 1.8rem !important;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }
        .feature-card {
            padding: 1.0rem;
            margin: 1.0rem 0;
            border-radius: 12px;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            min-height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .feature-title {
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 1.5rem;
            font-size: 1.75rem !important;
        }
        .feature-desc {
            color: #7f8c8d;
            font-size: 1.45rem !important;
            line-height: 1.4;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 4rem;
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
            background-color: #6c4db0 !important;
            color: #f8f9fa !important;
            border: none !important;
            cursor: not-allowed !important;
            opacity: 1 !important;
            font-weight: 600;
            border-radius: 4px;
        }
        .footer {
            text-align: center;
            padding: 0.5rem;
            margin-top: 2rem;
            color: #7f8c8d;
            font-size: 1.45rem;
            border-top: 2px solid;
            border-color: inherit;
        }
  
        [data-theme="light"] .footer {
            border-color: #2c3e50;
        }
   
        [data-theme="dark"] .footer {
            border-color: #ffffff;
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

        st.markdown('<h1 class="title">Customer Analytics</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Advanced tools to know and keep customers.</p>', unsafe_allow_html=True)

        # 🚀 Product Hunt Badge embedded here
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 2rem;">
                <a href="https://www.producthunt.com/products/xyz-bank-customer-churn-predictor?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-xyz&#0045;bank&#0045;customer&#0045;churn&#0045;predictor" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=986620&theme=neutral&t=1751464652612" alt="XYZ&#0032;Bank&#0032;Customer&#0032;Churn&#0032;Predictor - AI&#0045;Powered&#0032;Bank&#0032;Customer&#0032;Churn&#0032;Insights&#0044;&#0032;Automated&#0032;Retention | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Churn Model</div>
                        <div class="feature-desc">Spot customers at risk of leaving with our machine learning models.</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Client Intel</div>
                        <div class="feature-desc">Understand customer behavior patterns and product preferences.</div>
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Loyalty Tactics</div>
                        <div class="feature-desc">Drive customer loyalty with personalized recommendations.</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">KPI Tracker</div>
                        <div class="feature-desc">Track key indicators of customer satisfaction and engagement.</div>
                    </div>
                    """, unsafe_allow_html=True)

        is_authenticated = st.session_state.get("authenticated", False)

        if is_authenticated:
            if st.button("🔄 Launch Churn Prediction Tool", key="churn_button"):
                st.session_state.page = "Dashboard"
                st.rerun()
            if st.button("📈 Launch Graphs Dashboard", key="graphs_button"):
                st.session_state.page = "Graphs"
                st.rerun()
        else:
            st.button("🔒 Log in to access Churn Tool", disabled=True)
            st.button("🔒 Log in to access Churn Graphs", disabled=True)

    st.markdown("""
    <div class="footer">
        <p>© 2025 XYZ Bank Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()