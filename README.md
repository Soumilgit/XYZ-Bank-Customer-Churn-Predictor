# Bank Customer Churn Predictor

## Architecture
![Screenshot 2025-06-23 173901](https://github.com/user-attachments/assets/0096ae5f-3d94-4659-bb1f-0a1b5e2b3844)

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
- With Python, HTML-CSS, SQLite & EmailJS, it ingests 4000 customer data entries to predict churn risk with visual insights and AI-generated explanations/emails.

## Database
https://github.com/user-attachments/assets/af1fa292-a299-4aca-bb1e-174fd63661f3

## Quick Start
1. Clone repo  
2. `pip install -r requirements.txt`  
3. Add Groq & EmailJS API keys to `secrets.toml` file under a new `.streamlit` folder  
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
