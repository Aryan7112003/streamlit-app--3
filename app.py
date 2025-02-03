import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the pre-trained model
model = load_model("apple_stock_lstm_model.h5")

# Function to create sequences
def create_sequences(data, seq_len):
    X = []
    y = []
    
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i, 0])  # Sequence of 'seq_len' time steps
        y.append(data[i, 0])  # The next time step (target)
    
    return np.array(X), np.array(y)

# App title
st.title("Apple Stock Price Prediction using LSTM")

# File uploader for CSV
uploaded_file = st.file_uploader("Choose a CSV file with stock data", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    data = pd.read_csv(uploaded_file)

    # Check for proper columns (assuming 'Date' and 'Close' columns)
    if 'Date' in data.columns and 'Close' in data.columns:
        # Convert 'Date' column to datetime
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Display the first few rows of the data
        st.write("Data Preview:", data.head())

        # Create sequences (no scaling)
        SEQ_LEN = 60
        X, y = create_sequences(data[['Close']].values, SEQ_LEN)

        # Predict on the last sequence and predict the next 5 days
        last_sequence = X[-1].reshape(1, SEQ_LEN, 1)
        predicted_prices = []

        for i in range(5):  # Predicting the next 5 days
            pred = model.predict(last_sequence)
            predicted_prices.append(pred[0, 0])
            last_sequence = np.append(last_sequence[:, 1:, :], pred.reshape(1, 1, 1), axis=1)

        # Generate dates for the next 5 days
        next_dates = [datetime.today() + timedelta(days=i) for i in range(1, 6)]
        next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

        # Plot predictions
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(data.index, data['Close'], label="Actual Prices", color='blue')
        ax.plot(np.arange(len(data), len(data) + 5), predicted_prices, label="Predicted Prices (Next 5 Days)", color='red')
        ax.set_xticks(np.arange(len(data), len(data) + 5))
        ax.set_xticklabels(next_dates_str)
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock Price")
        ax.legend()
        st.pyplot(fig)

        # Display the predicted prices for the next 5 days
        predicted_df = pd.DataFrame({
            'Date': next_dates_str,
            'Predicted Price': predicted_prices
        })
        st.write(predicted_df)
    else:
        st.error("The CSV file must contain 'Date' and 'Close' columns.")
