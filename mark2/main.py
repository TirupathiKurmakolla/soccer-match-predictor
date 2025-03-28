import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Load the saved model
model = load_model('best_model.keras')

# Load the dataset to fit the scaler
data = pd.read_csv('dataset.csv')  # Make sure to provide the correct path

# Feature selection for scaler fitting
features = ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 
            'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
scaler = MinMaxScaler()
scaler.fit(data[features])

# Streamlit interface
st.title('Soccer Match Outcome Predictor')

# User input for features
input_data = []
for feature in features:
    input_data.append(st.number_input(feature.replace('_', ' '), min_value=0))

# Prediction
if st.button('Predict Outcome'):
    input_features = np.array([input_data])
    input_features_scaled = scaler.transform(input_features)
    input_features_scaled = input_features_scaled.reshape((input_features_scaled.shape[0], 1, input_features_scaled.shape[1]))

    prediction = model.predict(input_features_scaled)
    outcome = np.argmax(prediction, axis=1)
    
    if outcome == 0:
        st.write('Predicted Outcome: Away Win')
    elif outcome == 1:
        st.write('Predicted Outcome: Home Win')
    else:
        st.write('Predicted Outcome: Draw')
