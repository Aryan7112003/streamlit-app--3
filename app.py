import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# App title
st.title("Stock Price Prediction (Simple Moving Average)")

# File uploader for CSV
uploaded_file = st.file_uploader("Choose a CSV file with stock data", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    data = pd.read_csv(uploaded_file)

    # Display columns and first few rows for debugging
    st.write("Columns in the uploaded file:", data.columns)
    st.write("First few rows of the uploaded data:", data.head())

    # Automatically clean and convert all columns to numeric (ignoring errors)
    # This will remove any dollar signs, commas, etc., and convert columns to numeric
    data_cleaned = data.apply(pd.to_numeric, errors='coerce', axis=0)

    # Check if there are any numeric columns after cleaning
    numeric_columns = data_cleaned.select_dtypes(include=[np.number]).columns

    if len(numeric_columns) == 0:
        st.error("No numeric columns found in the CSV file.")
    else:
        # Use the first numeric column for analysis
        target_column = numeric_columns[0]

        # Display the selected column for clarity
        st.write(f"Using column '{target_column}' for analysis.")

        # Calculate the moving average (e.g., 5-day window)
        window_size = 5
        data_cleaned['Moving_Avg'] = data_cleaned[target_column].rolling(window=window_size).mean()

        # Drop rows with NaN values in the moving average column
        data_cleaned.dropna(subset=['Moving_Avg'], inplace=True)

        # Display the first few rows of the data after processing
        st.write("Data Preview after cleaning:", data_cleaned.head())

        # Predict the next 5 days (using the last moving average value)
        last_moving_avg = data_cleaned['Moving_Avg'].iloc[-1]
        predicted_prices = [last_moving_avg] * 5  # Simple assumption: next 5 days will follow the last moving average

        # Generate dates for the next 5 days
        next_dates = [datetime.today() + timedelta(days=i) for i in range(1, 6)]
        next_dates_str = [date.strftime('%Y-%m-%d') for date in next_dates]

        # Create DataFrame for predicted values to display in chart
        prediction_data = data_cleaned[[target_column, 'Moving_Avg']].copy()
        prediction_data = prediction_data.append(pd.DataFrame({
            target_column: predicted_prices,
            'Moving_Avg': [last_moving_avg] * 5
        }, index=pd.to_datetime(next_dates_str)))

        # Use Streamlit's native line chart
        st.line_chart(prediction_data[['Moving_Avg', target_column]])

        # Display the predicted prices for the next 5 days
        predicted_df = pd.DataFrame({
            'Date': next_dates_str,
            'Predicted Price': predicted_prices
        })
        st.write(predicted_df)
