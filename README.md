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
