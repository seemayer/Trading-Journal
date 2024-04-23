# app.py
import streamlit as st
import pandas as pd
import yfinance as yf
from st_aggrid import AgGrid

# Fetch real-time stock data
def fetch_stock_data():
    ticker = yf.Ticker('AAPL')  # Replace with your desired stock symbol
    data = ticker.history(period='1d', interval='1m')  # Fetch minute-level data
    return data

# Load data initially
stock_data = fetch_stock_data()

# Streamlit app
st.title("Real-Time Stock Prices")
st.write("Data updates every minute.")

# Display data in AG Grid
AgGrid(stock_data)

# Periodically update data
#while True:
stock_data = fetch_stock_data()
st.rerun()  # Rerun the app to update the displayed data
