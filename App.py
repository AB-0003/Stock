import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Title of the app
st.title("Stock Price Analysis App")

# Sidebar for user input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2025-01-01'))

# Fetch stock data from Yahoo Finance
st.sidebar.text("Fetching data...")
data = yf.download(ticker, start=start_date, end=end_date)

# Show raw data in a DataFrame
st.write(f"### {ticker} Stock Data", data)

# Plotting closing price with Matplotlib
st.write("### Closing Price Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data.index, data['Close'], label='Closing Price', color='blue')  # Ensure data['Close'] is 1D
ax.set_title(f"{ticker} - Closing Price")
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.legend()
st.pyplot(fig)

# Plotting Moving Average with Matplotlib
st.write("### 50-Day and 200-Day Moving Average")
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data.index, data['Close'], label='Closing Price', color='blue')
ax.plot(data.index, data['50_MA'], label='50-Day Moving Average', color='red')
ax.plot(data.index, data['200_MA'], label='200-Day Moving Average', color='green')
ax.set_title(f"{ticker} - Moving Averages")
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.legend()
st.pyplot(fig)


# Calculate daily returns
data['Daily Return'] = data['Close'].pct_change()

# Show daily returns in DataFrame
st.write("### Daily Returns", data['Daily Return'].tail())

# Plotting daily returns with Plotly
fig = px.histogram(data, x=data['Daily Return'], title=f"{ticker} Daily Returns Distribution", labels={'x': 'Daily Return'})
st.plotly_chart(fig)
