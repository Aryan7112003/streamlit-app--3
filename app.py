import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# App title
st.title("Apple Stock Market Price & Prediction")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload Apple Stock Data CSV", type="csv")

if uploaded_file is not None:
    # Load CSV file
    data = pd.read_csv(uploaded_file, skiprows=2)  # Skipping first 2 rows

    # Rename the first column to "Date"
    data.rename(columns={'Price': 'Date'}, inplace=True)

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Ensure numeric columns are properly formatted
    numeric_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Drop any remaining NaN values
    data.dropna(inplace=True)

    # Display the first few rows of the cleaned data
    st.write("Data Preview:", data.head())

    # Get today's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Get today's market price
    latest_data = data[data['Date'] == data['Date'].max()]
    
    if not latest_data.empty:
        today_price = latest_data.iloc[0]['Close']
        st.subheader(f"Today's Market Price ({today_date}): **${today_price:.2f}**")
    else:
        st.warning("No data available for today's market price.")

    # Calculate 5-day moving average for prediction
    window_size = 5
    data['Moving_Avg'] = data['Close'].rolling(window=window_size).mean()

    # Predict next 5 days (based on last moving average)
    last_moving_avg = data['Moving_Avg'].iloc[-1] if not data.empty else None
    predicted_prices = [last_moving_avg] * 5 if last_moving_avg is not None else [0] * 5

    # Generate dates for the next 5 days
    next_dates = [data['Date'].max() + timedelta(days=i) for i in range(1, 6)]
    next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

    # Create DataFrame for prediction
    predicted_df = pd.DataFrame({
        'Date': next_dates_str,
        'Predicted Price': predicted_prices
    })

    # Plot actual and predicted prices using Streamlit's line chart
    st.subheader("Stock Price Trend")
    chart_data = data[['Date', 'Close', 'Moving_Avg']].set_index('Date')
    st.line_chart(chart_data)

    # Display predicted prices for the next 5 days
    st.subheader("Predicted Prices for the Next 5 Days")
    st.write(predicted_df)
