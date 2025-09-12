import streamlit as st
import pandas as pd
import pickle
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from scipy.stats import percentileofscore
import utils as ut
import re
from sklearn.preprocessing import MinMaxScaler

ut.apply_sidebar_styles()

def main():
    st.sidebar.markdown("---")
    st.sidebar.header("Bank Customer Churn Prediction")

    load_dotenv()

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"],
    )

    @st.cache_resource
    def load_model(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    xgboost_model = load_model('models/xgb_model.pkl')
    naive_bayes_model = load_model('models/nb_model.pkl')
    random_forest_model = load_model('models/rf_model.pkl')
    svm_model = load_model('models/svm_model.pkl')
    voting_classifier_model = load_model('models/voting_clf.pkl')
    xgboost_SMOTE_model = load_model('models/xgboost-SMOTE.pkl')
    xgboost_featureEngineered_model = load_model('models/xgboost-featureEngineered.pkl')

    def prepare_input(credit_score, location, gender, age, tenure, balance,
                      num_of_products, has_credit_card, is_active_member,
                      estimated_salary):
        tenure_age_ratio = tenure / age if age != 0 else 0
        clv = (balance * tenure) / (age + 1)

        age_group_middleage = 1 if 30 <= age < 50 else 0
        age_group_senior = 1 if 50 <= age < 65 else 0
        age_group_elderly = 1 if age >= 65 else 0

        input_dict = {
            'CreditScore': credit_score,
            'Age': age,
            'Tenure': tenure,
            'Balance': balance,
            'NumOfProducts': num_of_products,
            'HasCrCard': int(has_credit_card),
            'IsActiveMember': int(is_active_member),
            'EstimatedSalary': estimated_salary,
            'Geography_Japan': 1 if location == "Japan" else 0,
            'Geography_USA': 1 if location == "USA" else 0,
            'Geography_Australia': 1 if location == "Australia" else 0,
            'Gender_Male': 1 if gender == "Male" else 0,
            'Gender_Female': 1 if gender == "Female" else 0,
            'CLV': clv,
            'TenureAgeRatio': tenure_age_ratio,
            'AgeGroup_Middleage': age_group_middleage,
            'AgeGroup_Senior': age_group_senior,
            'AgeGroup_Elderly': age_group_elderly,
        }

        smote_features = xgboost_SMOTE_model.get_booster().feature_names
        engineered_features = xgboost_featureEngineered_model.get_booster().feature_names

        input_df_smote = pd.DataFrame([input_dict])[smote_features]
        input_df_engineered = pd.DataFrame([input_dict])[engineered_features]

        basic_features = [
            'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
            'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
            'Geography_Japan', 'Geography_USA', 'Geography_Australia',
            'Gender_Male', 'Gender_Female'
        ]
        input_df_basic = pd.DataFrame([input_dict])[basic_features]

        return {
            'basic': input_df_basic,
            'smote': input_df_smote,
            'engineered': input_df_engineered,
            'dict': input_dict
        }

    def calculate_percentiles(df, input_dict):
        percentiles = {}
        for feature in input_dict:
            if feature in ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts'] and feature in df.columns:
                value = input_dict[feature]
                percentiles[feature] = percentileofscore(df[feature], value, kind='mean')
        return percentiles
    
    def get_voting_score(model, X):
        if hasattr(model, "predict_proba"):
            return model.predict_proba(X)[0][1]
        elif hasattr(model, "decision_function"):
            from scipy.special import expit
            return expit(model.decision_function(X))[0]
        else:
            est_outputs = []
            for est in model.estimators_:
                if hasattr(est, "predict_proba"):
                    est_outputs.append(est.predict_proba(X)[0][1])
                elif hasattr(est, "decision_function"):
                    from scipy.special import expit
                    est_outputs.append(expit(est.decision_function(X))[0])
                else:
                    est_outputs.append(float(est.predict(X)[0]))
            return float(np.mean(est_outputs))

    def get_nb_score(model, X):
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X) 
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_scaled)[0][1]
            proba = np.clip(proba, 1e-3, 1 - 1e-3) 
            return float(proba)
        else:
            return float(model.predict(X_scaled)[0])
        
    def make_predictions(input_dfs, customer_percentiles):
        probabilities = {
            'XGBoost': xgboost_model.predict_proba(input_dfs['basic'])[0][1],
            'Naive Bayes': get_nb_score(naive_bayes_model, input_dfs['basic']),
            'Random Forest': random_forest_model.predict_proba(input_dfs['basic'])[0][1],
            'SVM': svm_model.predict_proba(input_dfs['basic'])[0][1],
            'XGBoost SMOTE': xgboost_SMOTE_model.predict_proba(input_dfs['smote'])[0][1],
            'XGBoost Feature Engineered': xgboost_featureEngineered_model.predict_proba(input_dfs['engineered'])[0][1],
            'Voting Classifier': get_voting_score(voting_classifier_model, input_dfs['engineered'])
        }

        avg_probability = np.mean(list(probabilities.values()))

        col1, col2 = st.columns(2)
        with col1:
            fig = ut.create_gauge_chart(avg_probability)
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"The customer has a {avg_probability:.2%} probability of churning.")

        with col2:
            fig_probs = ut.create_model_probability_chart(probabilities)
            st.plotly_chart(fig_probs, use_container_width=True)

        percentile_chart = ut.create_percentile_bar_chart(customer_percentiles)
        st.plotly_chart(percentile_chart, use_container_width=True)

        return avg_probability

    def clean_response(text):
        return re.sub(r'<[^>]+>', '', text).strip()

    def explain_prediction(probability, input_dict, surname):
        prompt = f"""
        # CONTEXT #
        You are an expert data scientist at a bank, where you specialize in interpreting and explaining predictions of machine learning models.
        Your machine learning model has predicted that a customer named {surname} has a {round(probability * 100, 1)}% probability of churning, based on the information provided below.
        Here is the customer's information:
        {input_dict}
        Here are the machine learning model's top 10 most important features for predicting churns:
          Features         |    Importance
        ---------------------------------------
          CreditScore      |    0.039948
          Age              |    0.093195
          Tenure           |    0.038620
          Balance          |    0.052420
          NumOfProducts    |    0.354507
          HasCrCard        |    0.040686
          IsActiveMember   |    0.135773
          EstimatedSalary  |    0.035773
          Geography_Japan  |    0.042271
          Geography_USA    |    0.068507
       Geography_Australia |    0.040899
          Gender_Female    |    0.057401
          Gender_Male      |    0.000000

        {pd.set_option('display.max_columns', None)}

        Here are summary statistics for churned customers:
        {df[df['Exited'] == 1].describe()}

        Here are summary statistics for non-churned customers:
        {df[df['Exited'] == 0].describe()}

         # STYLE #
        Do NOT show your thought process. Only return the final answer. No planning. No explanation of features. No discussion of model logic.
        Only return the explanation text that would be shown to a customer-facing representative.

        # OBJECTIVE #
        - If {surname} is over 40% risk of churning, explain why by emphasizing behavioral patterns and tendencies common among customers with similar profiles.
        - If {surname} is not over 40% risk of churning, explain why by focusing on aspects that typically indicate stability or satisfaction.

        # AUDIENCE #
        Direct this explanation towards users who do not have much knowledge of the background details of {surname} and how those details are working together. Don't include any jargon or references to any of the data used to derive the explanation.

        # RESPONSE #
        Avoid direct references to any specific figures, statistical terms, category names, probabilities, model, models, top 10 most important features, or technical jargon.Your output must be only the final explanation paragraph. Nothing else. Keep the explanation to under 4 sentences.
        """
        raw_response = client.chat.completions.create(
            model='qwen/qwen3-32b',
            messages=[{"role": "user", "content": prompt}],
        )
        return clean_response(raw_response.choices[0].message.content)

    def generate_email(input_dict, explanation, surname):
        prompt = f"""
        # CONTEXT #
        You are a manager at XYZ Bank. You are responsible for ensuring customers stay with the bank and are incentivized with various offers.
        You noticed a customer named {surname} might be considering leaving the bank.
        Here is the customer's information:
        {input_dict}
        Here is some explanation as to why the customer might be at risk of churning:
        {explanation}
        
        # OBJECTIVE #
        Write a professional email to the customer that:
        - Thanks them for their loyalty
        - Offers personalized incentives to stay
        - Is warm and customer-focused
        - Includes 3-4 specific, relevant incentives
        
        # RULES #
        - NEVER mention probability, models, or data analysis
        - ONLY return the final email text
        - No thought process or explanations
        - No headers or subject line
        - Sign with "XYZ Bank" on a new line
        
        # STYLE #
        - Professional but friendly tone
        - Short paragraphs (1-2 sentences)
        - Bullet points for incentives
        - Total length: 150-200 words
        """
        raw_response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return clean_response(raw_response.choices[0].message.content)

    st.title("Bank Customer Churn Prediction")

    df = pd.read_csv("churn.csv")

    customers = [f"{row['CustomerId']} - {row['Surname']}" for _, row in df.iterrows()]
    selected_customer_option = st.selectbox("Customer selection", customers)

    if selected_customer_option:
        selected_customer_id = int(selected_customer_option.split(' - ')[0])
        selected_surname = selected_customer_option.split(' - ')[1]
        selected_customer = df.loc[df['CustomerId'] == selected_customer_id].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=selected_customer['CreditScore'])
            location = st.selectbox("Location", ["Australia", "Japan", "USA"], index=["Australia", "Japan", "USA"].index(selected_customer["Geography"]))
            gender = st.radio("Gender", ["Male", "Female"], index=0 if selected_customer["Gender"] == "Male" else 1)
            age = st.number_input("Age", min_value=10, max_value=100, value=int(selected_customer["Age"]))
            tenure = st.number_input("Tenure (years)", min_value=0, max_value=50, value=int(selected_customer["Tenure"]))

        with col2:
            balance = st.number_input("Balance", min_value=0.0, value=float(selected_customer["Balance"]))
            min_products = st.number_input("Number of Products", min_value=1, max_value=10, value=int(selected_customer['NumOfProducts']))
            has_credit_card = st.checkbox("Has Credit Card", value=bool(selected_customer["HasCrCard"]))
            is_active_member = st.checkbox("Is Active Member", value=bool(selected_customer["IsActiveMember"]))
            estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=float(selected_customer["EstimatedSalary"]))

        input_dfs_and_dict = prepare_input(credit_score, location, gender, age, tenure, balance, min_products, has_credit_card, is_active_member, estimated_salary)

        percentiles = calculate_percentiles(df, input_dfs_and_dict['dict'])
        avg_probability = make_predictions(input_dfs_and_dict, percentiles)

        explanation = explain_prediction(avg_probability, input_dfs_and_dict['dict'], selected_surname)
        st.markdown("---")
        st.markdown("## Explanation of Prediction")
        st.markdown(explanation)

        email = generate_email(input_dfs_and_dict['dict'], explanation, selected_surname)
        st.markdown("---")
        st.markdown("## Personalized Email")
        st.markdown(email)

if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "homepage"

    if st.session_state.page == "homepage":
        main()
        
    elif st.session_state.page == "churn_prediction":
        import main_dashboard
        main_dashboard.main()
