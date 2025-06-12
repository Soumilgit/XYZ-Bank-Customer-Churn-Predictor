# Customer Churn Predictor

Bank customer churn prediction web app utilizing:

a. Decision Tree - Accuracy: 𝟳𝟵.𝟭𝟯%

b. K-Nearest Neighbors (KNN) - Accuracy: 𝟴𝟮%

c. Naive Bayes - Accuracy: 𝟴𝟮.𝟮𝟱%

d. Random Forest Classifier - Accuracy: 𝟴𝟯.𝟳𝟱%

e. Support Vector Machine (SVM) - Accuracy: 𝟴𝟰.𝟭𝟯%

f. XGBoost Classifier - Accuracy: 𝟴𝟰.𝟮𝟱%

g. XGBoost + SMOTE Classifier - Accuracy: 𝟴𝟯.𝟴𝟳%

h. Voting Classifier - Accuracy: 𝟴𝟯.𝟲𝟯%

i. Mistral Saba 24B LLM [OpenAI]  

Analyzes 4K customers to predict churn risk with visual insights and AI-generated explanations/emails.

## Quick Start
1. Clone repo  
2. `pip install -r requirements.txt`  
3. Add Groq API key to `secrets.toml` file under a new `.streamlit` folder  
4. `streamlit run Homepage.py`

## Research references - badges link to papers
<div style="display: flex; gap: 12px; align-items: center; margin: 15px 0;">
  <a href="https://www.researchgate.net/publication/340855263_Churning_of_Bank_Customers_Using_Supervised_Learning" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ResearchGate-00CCB?style=flat-square&logo=researchgate&logoColor=white&labelWidth=30&height=38" alt="Churning of Bank Customers Using Supervised Learning" style="height:32px;">
  </a>
  
  <a href="https://www.sciencedirect.com/science/article/pii/S2666764923000401" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ScienceDirect-F16521?style=flat-square&logo=Etsy&logoColor=white&labelWidth=30&height=38" alt="Investigating customer churn in banking: a machine learning approach and visualization app for data science and management" style="height:32px;">
  </a>
</div>
