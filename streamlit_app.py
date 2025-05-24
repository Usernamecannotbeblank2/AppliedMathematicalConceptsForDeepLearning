import streamlit as st
import tensorflow as tf
import numpy as np

st.title("Customer Churn Predictor 🚶‍♂️‍➡️")
st.markdown("---")

try:
    model = tf.keras.models.load_model('telco_churn_model_2.8.32_0.26_Isaac.keras')
except Exception as e:
    st.error(f'ERROR: {e}')
    st.stop()


gender = st.selectbox(
    "Gender:",
    ["Male", "Female"]
)

isSeniorCitizen = st.checkbox("Are you a senior citizen?")

isPartner = st.checkbox("Do you have a partner?")

isDependants = st.checkbox("Do you have dependants?")

tenture = st.number_input(
    "Tenture:",
    min_value=0,
    max_value=100,
    value=50,
    step=1
)

isPhoneService = st.checkbox("Are we your phone provider?")

isMultipleLines = False
if(isPhoneService):
    isMultipleLines = st.checkbox("Do you have more than one line with us?")

internetService = st.selectbox(
    "Do you use our internet service?",
    ["Yes, wireless", "Yes, fiber optic", "No"]
)

isOnlineSecurity = False
isOnlineBackup = False
if(internetService != "No"):
    isOnlineSecurity = st.checkbox("Do you use our online security service?")
    isOnlineBackup = st.checkbox("Do you use our online backup service?")

isDeviceProtected = st.checkbox("Do you have device protection?")

isTechSupport = st.checkbox("Do you have technical support?")

isStreamingTV = st.checkbox("Do you have our TV streaming service?")
isStreamingMovies = st.checkbox("Do you have our movie streaming service?")

contract = st.selectbox(
    "Contract Period:",
    ["Month-to-month", "One year", "Two year"]
)

isPaperless = st.checkbox("Do you use paperless billing?")

paymentMethod = st.selectbox(
    "What is your method of payment:",
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
)

monthlyCharges = st.number_input(
    "Monthly Charges:",
    min_value=0,
    max_value=500,
    value=50,
    step=1
)


totalCharges = st.number_input(
    "Total Charges:",
    min_value=0,
    max_value=500,
    value=50,
    step=1
)

if st.button("Process"):
    #SHAPE -> ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges', 'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes', 'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'PhoneService_Yes', 'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No', 'OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes', 'TechSupport_Yes', 'StreamingTV_Yes', 'StreamingMovies_Yes']
    data = [
        1 if isSeniorCitizen else 0,
        1 if tenture else 0,
        1 if monthlyCharges else 0,
        1 if totalCharges else 0,
        1 if gender == 'Male' else 0,
        1 if isPartner else 0,
        1 if isDependants else 0,
        1 if contract == 'One year' else 0,
        1 if contract == 'Two year' else 0,
        1 if isPaperless else 0,
        1 if paymentMethod == 'Credit card (automatic)' else 0,
        1 if paymentMethod == 'Electronic check' else 0,
        1 if paymentMethod == 'Mailed check' else 0,
        1 if isPhoneService else 0,
        1 if isMultipleLines else 0,
        1 if internetService == 'Yes, fiber optic' else 0,
        1 if internetService == 'No' else 0,
        1 if isOnlineSecurity else 0,
        1 if isOnlineBackup else 0,
        1 if isDeviceProtected else 0,
        1 if isTechSupport else 0,
        1 if isStreamingTV else 0,
        1 if isStreamingMovies else 0
    ]

    data = np.array([data])
    prediction = model.predict(data)

    st.subheader("Prediction:")
    if prediction[0][0] > 0.5:
        st.write("the user will be staying with the company 😄")
    else:
        st.write("the user will be leaving us 😔")

