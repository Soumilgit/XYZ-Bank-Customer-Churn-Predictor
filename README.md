# Bank Customer Churn Predictor

## Architecture
![Screenshot 2025-07-07 221306](https://github.com/user-attachments/assets/c4c2474b-dc7c-42cb-9820-05627cb35349)

## Description + stats
- Bank customer churn prediction web app utilizing:
```
Decision Tree - Accuracy: 79.13%
K-Nearest Neighbors (KNN) - Accuracy: 82%
Naive Bayes - Accuracy: 82.25%
Random Forest Classifier - Accuracy: 83.75%
Support Vector Machine (SVM) - Accuracy: 84.13%
XGBoost Classifier - Accuracy: 84.25%
XGBoost + SMOTE Classifier - Accuracy: 83.87%
Voting Classifier - Accuracy: 83.63%
Mistral Saba 24B LLM [OpenAI]
```
- With Python, HTML-CSS-JS, Supabase & EmailJS, it ingests 4000 customer data entries to predict churn risk with visual insights and AI-generated explanations/emails.
- <code><ins>Custom Kaggle dataset, usability score <code>9.41</code>:<ins></code>
  <a href="https://www.kaggle.com/datasets/soumilmukhopadhyay/xyz-bank-customer-churn" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white&labelWidth=30&height=30" alt="Kaggle dataset" style="height:30px;">
  </a>

## Database
https://github.com/user-attachments/assets/346ee74b-fe51-4eb0-8a22-f988abfc73dd

## Quick Start
1. Clone repo  
2. `pip install -r requirements.txt`  
3. Add Groq, Supabase & EmailJS API keys to `secrets.toml` file under a new `.streamlit` folder  
4. `streamlit run main.py`

## Research references - badges link to papers
<div style="display: flex; gap: 12px; align-items: center; margin: 15px 0;">
  <a href="https://www.researchgate.net/publication/340855263_Churning_of_Bank_Customers_Using_Supervised_Learning" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ResearchGate-00CCB?style=flat-square&logo=researchgate&logoColor=white&labelWidth=30&height=38" alt="Churning of Bank Customers Using Supervised Learning" style="height:32px;">
  </a>
  
  <a href="https://www.sciencedirect.com/science/article/pii/S2666764923000401" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ScienceDirect-F16521?style=flat-square&logo=Etsy&logoColor=white&labelWidth=30&height=38" alt="Investigating customer churn in banking: a machine learning approach and visualization app for data science and management" style="height:32px;">
  </a>
</div>

## License
This project is licensed under the [MIT License](https://github.com/Soumilgit/Datathon_Team-DataP1ac3X.c0m/blob/main/LICENSE).
