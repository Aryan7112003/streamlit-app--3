import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
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

# User input for stock symbol
stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL)", "AAPL")

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# Download stock data up to today
data = yf.download(stock_symbol, start="2015-01-01", end=today)

# Display the first few rows of data
st.write("Data Preview:", data.head())

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['Close']].values)

# Create sequences
SEQ_LEN = 60
X, y = create_sequences(scaled_data, SEQ_LEN)

# Predict on the last sequence and predict the next 5 days
last_sequence = X[-1].reshape(1, SEQ_LEN, 1)
predicted_prices = []

for i in range(5):  # Predicting the next 5 days
    pred = model.predict(last_sequence)
    predicted_prices.append(pred[0, 0])
    last_sequence = np.append(last_sequence[:, 1:, :], pred.reshape(1, 1, 1), axis=1)

predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))

# Generate dates for the next 5 days
next_dates = [datetime.today() + timedelta(days=i) for i in range(1, 6)]
next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

# Plot predictions
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(np.arange(len(data)), scaler.inverse_transform(scaled_data), label="Actual Prices", color='blue')
ax.plot(np.arange(len(data), len(data) + 5), predicted_prices, label="Predicted Prices (Next 5 Days)", color='red')
ax.set_xticks(np.arange(len(data), len(data) + 5))
ax.set_xticklabels(next_dates_str)
ax.set_xlabel("Date")
ax.set_ylabel("Stock Price")
ax.legend()
st.pyplot(fig)

# Display the predicted prices for the next 5 days
st.write("Predicted Apple Stock Prices for the next 5 days:")
predicted_df = pd.DataFrame({
    'Date': next_dates_str,
    'Predicted Price': predicted_prices.flatten()
})
st.write(predicted_df)
