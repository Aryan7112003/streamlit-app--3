import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# App title
st.title("Apple Stock Price Prediction (Simple Moving Average)")

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

        # Calculate the moving average (e.g., 5-day window)
        window_size = 5
        data['Moving_Avg'] = data['Close'].rolling(window=window_size).mean()

        # Predict the next 5 days (using the last moving average value)
        last_moving_avg = data['Moving_Avg'].iloc[-1]
        predicted_prices = [last_moving_avg] * 5  # Simple assumption: next 5 days will follow the last moving average

        # Generate dates for the next 5 days
        next_dates = [datetime.today() + timedelta(days=i) for i in range(1, 6)]
        next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

        # Create a plot using Plotly
        fig = go.Figure()

        # Add actual prices and moving averages to the plot
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Prices', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Avg'], mode='lines', name='Moving Average', line=dict(color='green')))
        
        # Add predicted prices (next 5 days) to the plot
        fig.add_trace(go.Scatter(x=next_dates_str, y=predicted_prices, mode='lines', name='Predicted Prices (Next 5 Days)', line=dict(color='red')))

        # Update plot layout
        fig.update_layout(
            title="Apple Stock Price Prediction using Moving Average",
            xaxis_title="Date",
            yaxis_title="Stock Price",
            template="plotly_dark"
        )

        # Display the plot
        st.plotly_chart(fig)

        # Display the predicted prices for the next 5 days
        predicted_df = pd.DataFrame({
            'Date': next_dates_str,
            'Predicted Price': predicted_prices
        })
        st.write(predicted_df)
    else:
        st.error("The CSV file must contain 'Date' and 'Close' columns.")
