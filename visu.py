import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import requests
import json
import threading  # Import the threading module

TRANSACTIONS_FILE = 'transactions.json'

# Function to load existing transactions from file
def load_transactions():
    try:
        with open(TRANSACTIONS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to fetch and store real-time transactions
def fetch_and_store_transactions():
    while True:
        try:
            response = requests.get('http://127.0.0.1:5000/transactions')
            transactions_data = response.json().get('transactions', [])

            save_transactions(transactions_data)

            time.sleep(60)  # Fetch data every 1 minute
        except Exception as e:
            print(f"Error fetching transactions: {str(e)}")
            time.sleep(60)  # Retry after 1 minute in case of an error

# Function to save transactions to file
def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'w') as file:
        json.dump(transactions, file, indent=2)

# Function to create real-time transaction visualizations
def create_transaction_visualizations():
    st.markdown("## Real-Time Transaction Visualizations")

    transactions = load_transactions()

    if not transactions:
        st.warning("No transactions available yet.")
        return

    df_transactions = pd.DataFrame(transactions)

    st.markdown("### Transaction History")
    st.dataframe(df_transactions)

    st.markdown("### Transaction Amount Distribution")
    fig_amount_distribution = px.histogram(df_transactions, x='amount', title='Transaction Amount Distribution')
    st.plotly_chart(fig_amount_distribution)

    st.markdown("### Transaction Time Series")
    df_transactions['timestamp'] = pd.to_datetime(df_transactions['timestamp'])
    fig_time_series = px.line(df_transactions, x='timestamp', y='amount', title='Transaction Time Series')
    st.plotly_chart(fig_time_series)

if __name__ == '__main__':
    st.set_page_config(
        page_title='Real-Time Transactions Dashboard',
        page_icon='💰',
        layout='wide'
    )

    st.title("Real-Time Transactions Dashboard")

    # Button to trigger money flow visualization
    if st.button("Money Flow Visualization"):
        create_transaction_visualizations()

    # Run the dashboard in the background using threading
    thread = threading.Thread(target=fetch_and_store_transactions)
    thread.start()