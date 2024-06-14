import requests
import json
from datetime import datetime, timedelta
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

TRANSACTIONS_FILE = 'transactions.json'
FAKE_TRANSACTIONS_FILE = 'fake_transactions.json'
MODEL_FILE = 'fake_transaction_model.joblib'

# Function to load existing transactions from file
def load_transactions():
    try:
        with open(TRANSACTIONS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save transactions to file
def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'w') as file:
        json.dump(transactions, file, default=str, indent=2)

# Function to load existing fake transactions from file
def load_fake_transactions():
    try:
        with open(FAKE_TRANSACTIONS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save fake transactions to file
def save_fake_transactions(fake_transactions):
    with open(FAKE_TRANSACTIONS_FILE, 'w') as file:
        json.dump(fake_transactions, file, default=str, indent=2)

# Function to preprocess data for training
def preprocess_data(transactions):
    X = []
    y = []

    for i, transaction in enumerate(transactions):
        sender_id = transaction['sender_user_id']
        amount = transaction['amount']
        timestamp = datetime.strptime(transaction['timestamp'], '%Y-%m-%dT%H:%M:%S')

        # Extract features 
        features = [sender_id, amount, timestamp.timestamp()]

        # Check for the logic: money sent from the same account to many accounts at various locations in very little time
        if i > 0:
            previous_transaction = transactions[i - 1]
            if sender_id == previous_transaction['sender_user_id'] and amount == previous_transaction['amount'] and \
               timestamp - datetime.strptime(previous_transaction['timestamp'], '%Y-%m-%dT%H:%M:%S') < timedelta(minutes=1):
                label = 1  # Fake transaction
            else:
                label = 0  # Not fake transaction
        else:
            label = 0  # Not fake transaction

        X.append(features)
        y.append(label)

    return X, y

# Function to fetch and store real-time transactions
def fetch_and_store_transactions():
    while True:
        try:
            response = requests.get('http://127.0.0.1:5000/transactions')
            transactions_data = response.json().get('transactions', [])

            existing_transactions = load_transactions()
            existing_transactions.extend(transactions_data)

            print(f"Total Transactions: {len(existing_transactions)}")

            # Detect fake transactions using the trained model
            X, y = preprocess_data(existing_transactions)
            model = train_model(X, y)
            fake_transactions = detect_fake_transactions(existing_transactions, model)

            if fake_transactions:
                print("Fake Transactions Detected:")
                for fake_transaction in fake_transactions:
                    print(json.dumps(fake_transaction, default=str, indent=2))

            # Save transactions and fake transactions
            save_transactions(existing_transactions)
            save_fake_transactions(fake_transactions)

            time.sleep(60)  # Fetch data every 1 minute
        except Exception as e:
            print(f"Error fetching transactions: {str(e)}")
            time.sleep(60)  # Retry after 1 minute in case of an error

# Function to train the machine learning model
def train_model(X, y):
    model = make_pipeline(StandardScaler(), RandomForestClassifier())
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    return model

# Function to detect fake transactions using the trained model
def detect_fake_transactions(transactions, model):
    X, _ = preprocess_data(transactions)
    predictions = model.predict(X)

    fake_transactions = [transaction for transaction, prediction in zip(transactions, predictions) if prediction == 1]

    return fake_transactions

if __name__ == '__main__':
    fetch_and_store_transactions()