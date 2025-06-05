# import streamlit as st
# import joblib
#
# # Load the model and vectorizer
# model = joblib.load(r"D:\Fake News Detection\models trained\ensemble_meta_model_updated.joblib")
# vectorizer = joblib.load(r"D:\Fake News Detection\models trained\tfidf_vectorizer.joblib")  # Update this to the actual path
#
# # Define the prediction function
# def predict_fake_news(news_text):
#     # Transform the input text to numeric format using the vectorizer
#     transformed_text = vectorizer.transform([news_text])  # Vectorizes the text input
#     prediction = model.predict(transformed_text)
#     return "Fake" if prediction == 0 else "Real"
#
# # Streamlit UI
# st.title("Fake News Detection")
# st.write("Enter the news text below to check if it's fake or real:")
#
# # Input text area
# news_text = st.text_area("News Text")
#
# # Predict button
# if st.button("Check"):
#     if news_text:
#         prediction = predict_fake_news(news_text)
#         st.write(f"The news is predicted to be: **{prediction}**")
#     else:
#         st.write("Please enter some text to analyze.")


import streamlit as st
import joblib
import pandas as pd

# Load the base models, vectorizer, and meta-model
svm_model = joblib.load(r"D:\Fake News Detection\models trained\svm_model.joblib")
logreg_model = joblib.load(r"D:\Fake News Detection\models trained\logreg_model.joblib")
vectorizer = joblib.load(r"D:\Fake News Detection\models trained\tfidf_vectorizer.joblib")
meta_model = joblib.load(r"D:\Fake News Detection\models trained\ensemble_meta_model_updated.joblib")


# Define the prediction function
def predict_fake_news(news_text):
    # Transform the input text to numeric format using the TF-IDF vectorizer
    transformed_text = vectorizer.transform([news_text])  # Vectorizes the text input

    # Get probabilities from the SVM and Logistic Regression models
    svm_prob = svm_model.predict_proba(transformed_text)[:, 1][0]  # Positive class probability for SVM
    logreg_prob = logreg_model.predict_proba(transformed_text)[:, 1][
        0]  # Positive class probability for Logistic Regression

    # Combine these probabilities into a DataFrame with the expected format for meta-model
    stacked_probs = pd.DataFrame({
        'svm_probs': [svm_prob],
        'logreg_probs': [logreg_prob]
    })

    # Get the final prediction from the meta-model
    prediction = meta_model.predict(stacked_probs)[0]
    return "Real" if prediction == 1 else "Fake"


# Streamlit UI
st.title("Fake News Detection")
st.write("Enter the news text below to check if it's fake or real:")

# Input text area
news_text = st.text_area("News Text")

# Predict button
if st.button("Check"):
    if news_text:
        prediction = predict_fake_news(news_text)
        st.write(f"The news is predicted to be: **{prediction}**")
    else:
        st.write("Please enter some text to analyze.")
