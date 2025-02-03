import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# App title
st.title("Apple Stock Market Price & Prediction")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload Apple Stock Data CSV", type="csv")

if uploaded_file is not None:
    # Load CSV file and skip the first 2 rows (as per your file format)
    data = pd.read_csv(uploaded_file, skiprows=2)

    # Print column names for debugging
    st.write("Actual Column Names in CSV:", list(data.columns))

    # Rename the first column to "Date" (Ensure this matches your actual column name)
    if "Price" in data.columns:
        data.rename(columns={'Price': 'Date'}, inplace=True)

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Find the actual numeric columns (handle missing ones)
    available_columns = [col for col in ['Close', 'High', 'Low', 'Open', 'Volume'] if col in data.columns]

    # Ensure numeric columns are properly formatted
    for col in available_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Drop any remaining NaN values
    data.dropna(subset=available_columns, inplace=True)

    # Display the first few rows of the cleaned data
    st.write("Data Preview (Cleaned):", data.head())

    # Get today's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Get today's market price (Check if "Close" exists)
    if "Close" in data.columns:
        latest_data = data[data['Date'] == data['Date'].max()]
        if not latest_data.empty:
            today_price = latest_data.iloc[0]['Close']
            st.subheader(f"Today's Market Price ({today_date}): **${today_price:.2f}**")
        else:
            st.warning("No data available for today's market price.")
    else:
        st.error("Column 'Close' not found in the CSV file.")

    # Calculate 5-day moving average if 'Close' exists
    if "Close" in data.columns:
        window_size = 5
        data['Moving_Avg'] = data['Close'].rolling(window=window_size).mean()

        # Predict next 5 days (based on last moving average)
        last_moving_avg = data['Moving_Avg'].dropna().iloc[-1] if not data.empty else None
        predicted_prices = [last_moving_avg] * 5 if last_moving_avg is not None else [0] * 5

        # Generate dates for the next 5 days
        next_dates = [data['Date'].max() + timedelta(days=i) for i in range(1, 6)]
        next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

        # Create DataFrame for prediction
        predicted_df = pd.DataFrame({'Date': next_dates_str, 'Predicted Price': predicted_prices})

        # Plot actual and predicted prices using Streamlit's line chart
        st.subheader("Stock Price Trend")
        if 'Moving_Avg' in data.columns:
            chart_data = data[['Date', 'Close', 'Moving_Avg']].set_index('Date')
            st.line_chart(chart_data)

        # Display predicted prices for the next 5 days
        st.subheader("Predicted Prices for the Next 5 Days")
        st.write(predicted_df)
