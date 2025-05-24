import streamlit as st
import tensorflow as tf
import numpy as np

st.title("Customer Churn Predictor 🚪🚶‍♂️‍➡️")
st.markdown("---")

try:
    model = tf.keras.models.load_model('telco_churn_model_2.8.32_0.26_Isaac.keras')
except Exception as e:
    st.error(f'ERROR: {e}')
    st.stop()

st.subheader("General info")

gender = st.selectbox(
    "Gender:",
    ["Male", "Female"]
)

tenure = st.number_input(
    "Tenure:",
    min_value=0,
    max_value=100,
    value=30,
    step=10
)

isSeniorCitizen = st.checkbox("Senior citizen")

isPartner = st.checkbox("Has partner")

isDependants = st.checkbox("Dependents")

st.markdown("---")
st.subheader("Phone Service")

isPhoneService = st.checkbox("Uses our phone service")

isMultipleLines = False
if(isPhoneService):
    isMultipleLines = st.checkbox("More than one line")

st.markdown("---")
st.subheader("Internet Service")

internetService = st.selectbox(
    "Uses our internet service",
    ["Yes, DSL", "Yes, fiber optic", "No"],
    index=2 
)

isOnlineSecurity = False
isOnlineBackup = False
isDeviceProtected = False
isTechSupport = False
isStreamingTV = False
isStreamingMovies = False
if(internetService != "No"):
    isOnlineSecurity = st.checkbox("Online security service")
    isOnlineBackup = st.checkbox("Online backup service")
    isDeviceProtected = st.checkbox("Device protection")
    isTechSupport = st.checkbox("Technical support")
    isStreamingTV = st.checkbox("TV streaming service")
    isStreamingMovies = st.checkbox("Movie streaming service")

st.markdown("---")
st.subheader("Billing")

isPaperless = st.checkbox("Paperless billing")

contract = st.selectbox(
    "Contract period type",
    ["Month-to-month", "One year", "Two year"]
)

paymentMethod = st.selectbox(
    "Payment method",
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
)

monthlyCharges = st.number_input(
    "Monthly Charges",
    min_value=0.00,
    max_value=200.00,
    value=50.00,
    step=10.00,
    format="%.2f"
)

totalCharges = st.number_input(
    "Total Charges",
    min_value=0.00,
    max_value=9000.00,
    value=2000.00,
    step=100.00,
    format="%.2f"
)

if st.button("Process"):
    # SHAPE ORDER -> ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges', 'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes', 'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'PhoneService_Yes', 'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No', 'OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes', 'TechSupport_Yes', 'StreamingTV_Yes', 'StreamingMovies_Yes']
    data = [
        isSeniorCitizen,
        tenure,
        monthlyCharges,
        totalCharges,
        1 if gender == 'Male' else 0,
        isPartner,
        isDependants,
        1 if contract == 'One year' else 0,
        1 if contract == 'Two year' else 0,
        isPaperless,
        1 if paymentMethod == 'Credit card (automatic)' else 0,
        1 if paymentMethod == 'Electronic check' else 0,
        1 if paymentMethod == 'Mailed check' else 0,
        isPhoneService,
        isMultipleLines,
        1 if internetService == 'Yes, fiber optic' else 0,
        1 if internetService == 'No' else 0,
        isOnlineSecurity,
        isOnlineBackup,
        isDeviceProtected,
        isTechSupport,
        isStreamingTV,
        isStreamingMovies
    ]

    data = np.array([data])
    prediction = model.predict(data)

    st.subheader("Prediction:")
    st.text(prediction[0][0]) # for testing 
    if prediction[0][0] > 0.5:
        st.write("the user will be staying with the company 😄")
    else:
        st.write("the user will be leaving us 😔")
