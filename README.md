# Bank Customer Churn Predictor

## Architecture
<img width="1221" height="828" alt="image" src="https://github.com/user-attachments/assets/0134b4fc-7d84-4eaf-aea4-5eef61e87569" />

## Description + stats
- A full-stack bank customer churn predictor application utilizing:

| Name of model                        | Accuracy   |
|--------------------------------------|------------|
| Decision Tree                        | 79.13%     |
| K-Nearest Neighbors (KNN)            | 82.00%     |
| Naive Bayes                          | 82.25%     |
| Random Forest Classifier             | 83.75%     |
| Support Vector Machine (SVM)         | 84.13%     |
| XGBoost Classifier                   | 84.25%     |
| XGBoost + SMOTE Classifier           | 83.87%     |
| Voting Classifier                    | 83.63%     |
| Qwen3 32B LLM [OpenAI]               | —          |

- It ingests <code>4000</code> entries to predict churn risk with visual insights, AI-generated explanations and emails.

## Tech Stack

| Purpose              | Technologies |
|----------------------|--------------|
| **Core Tech** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=black) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=black) ![OpenAI](https://img.shields.io/badge/OpenAI-8968CD?style=for-the-badge&logo=openai&logoColor=black) ![Plotly](https://img.shields.io/badge/plotly-7A76FF?style=for-the-badge&logo=plotly&logoColor=black)|
| **Frontend & Framework** | ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=black) ![CSS](https://img.shields.io/badge/CSS3-0080FE?style=for-the-badge&logo=css&logoColor=black) ![JavaScript](https://img.shields.io/badge/JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=black) |
| **Backend + DB** | ![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=black) ![EmailJS](https://img.shields.io/badge/EmailJS-FF9A00?style=for-the-badge&logo=mailboxdotorg&logoColor=black) |
| **Other Libraries** |  ![NumPy](https://img.shields.io/badge/NumPy-7285A5?style=for-the-badge&logo=numpy&logoColor=black) ![Pandas](https://img.shields.io/badge/Pandas-A865B5?style=for-the-badge&logo=pandas&logoColor=black) ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=black) ![Pillow](https://img.shields.io/badge/Pillow-D3D3D3?style=for-the-badge&logo=imagedotsc&logoColor=black) |

## Database + authentication
https://github.com/user-attachments/assets/9aea195d-7073-4813-9a08-3648790b84ce

## Quick Start
1. Clone repo  
2. ```
   pip install -r requirements.txt
   ```  
3. Store below in a <ins>secrets.toml</ins> file under a <ins>.streamlit</ins> folder :
```
GROQ_API_KEY = ""
SUPABASE_URL = ""
SUPABASE_SERVICE_ROLE_KEY= ""
EMAILJS_PUBLIC_KEY= ""
EMAILJS_TEMPLATE_ID= ""
EMAILJS_SERVICE_ID= ""
```
4. ```
   streamlit run main.py
   ```

## Research references + custom dataset badge-links
<div style="display: flex; gap: 12px; align-items: center; margin: 15px 0;">
  <a href="https://www.researchgate.net/publication/340855263_Churning_of_Bank_Customers_Using_Supervised_Learning" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ResearchGate-00CCB?style=flat-square&logo=researchgate&logoColor=white&labelWidth=30&height=38" alt="Churning of Bank Customers Using Supervised Learning" style="height:32px;">
  </a>
  
  <a href="https://www.sciencedirect.com/science/article/pii/S2666764923000401" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/ScienceDirect-F16521?style=flat-square&logo=Etsy&logoColor=white&labelWidth=30&height=38" alt="Investigating customer churn in banking: a machine learning approach and visualization app for data science and management" style="height:32px;">
  </a>

  <a href="https://www.kaggle.com/datasets/soumilmukhopadhyay/xyz-bank-customer-churn" style="text-decoration: none;">
  <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white"
       alt="Kaggle dataset"
       style="height:34px; vertical-align: middle; margin-left: 1px;">
</a>
</div>

## License
This project is licensed under the [MIT License](https://github.com/Soumilgit/Datathon_Team-DataP1ac3X.c0m/blob/main/LICENSE).
