# Customer Churn Predictor
Bank customer churn prediction web app utilizing:
a. Decision Tree
b. K-Nearest Neighbors (KNN)
c. Naive Bayes
d. Random Forest
e. Support Vector Machine (SVM)
f. Classifier
g. XGBoost + SMOTE with feature engineering
h. Mistral Saba 24B LLM [OpenAI]

Analyzes 4K customers to predict churn risk with visual insights and AI-generated explanations/emails.

## Quick Start
Clone repo
`pip install -r requirements.txt`
Add Groq API key to `secrets.toml` file under a new `.streamlit` folder
`streamlit run Homepage.py`
