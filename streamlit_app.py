import streamlit as st
import tensorflow as tf

st.title("Customer Churn Predictor 🚶‍♂️‍➡️")
st.markdown("---")

try:
    model = tf.keras.models.load_model('telco_churn_model_2.8.32_0.26_Isaac.keras')
except Exception as e:
    st.error(f'ERROR: {e}')
    #st.stop()


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

isInternetService = st.checkbox("Are we your internet provider?")

isOnlineSecurity = False
isOnlineBackup = False
if(isInternetService):
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

#SHAPE -> ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges', 'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes', 'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'PhoneService_Yes', 'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No', 'OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes', 'TechSupport_Yes', 'StreamingTV_Yes', 'StreamingMovies_Yes']
if st.button("Process"):
    data = [
        isSeniorCitizen,
        tenture,
        monthlyCharges,
        totalCharges,
        gender.map({'Male': 1, 'Female': 0}),
        isPartner,
        isDependants,
        contract.map({'Month-to-month': 0, 'One year': 1, 'Two year': 0}),
        contract.map({'Month-to-month': 0, 'One year': 0, 'Two year': 1}),
        isPaperless,
        paymentMethod.map({'Electronic check': 0, 'Mailed check': 0, 'Bank transfer (automatic)': 0, 'Credit card (automatic)': 1}),
        paymentMethod.map({'Electronic check': 1, 'Mailed check': 0, 'Bank transfer (automatic)': 0, 'Credit card (automatic)': 0}),
        paymentMethod.map({'Electronic check': 0, 'Mailed check': 1, 'Bank transfer (automatic)': 0, 'Credit card (automatic)': 0}),
        isPhoneService,
        isMultipleLines,
        'InternetService_Fiber optic', #forgot this
        isInternetService,
        isOnlineSecurity,
        isOnlineBackup,
        isDeviceProtected,
        isTechSupport,
        isStreamingTV,
        isStreamingMovies
    ]

    prediction = model.predict(data)

    st.subheader("Prediction:")
    if prediction[0][0] > 0.5:
        st.write("the user will be staying with the company 😄")
    else:
        st.write("the user will be leaving us 😔")

